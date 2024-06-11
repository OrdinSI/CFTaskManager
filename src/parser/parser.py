import logging

import requests

from src.db.models.task import Subject, Task


class Parser:
    """ Class for parsing. """

    def __init__(self):
        pass

    async def parse(self):
        """ Main method. """
        try:
            results = await self.request_codeforces()

            if not results:
                return

            problems = results["problems"]
            problem_statistics = {f"{stat['contestId']}{stat['index']}": stat['solvedCount'] for stat in
                                  results["problemStatistics"]}

            tags_map = await self.get_tags_map()
            await self.process_tasks(problems, tags_map, problem_statistics)

        except Exception as e:
            logging.error(f"Ошибка при парсинге: {e}")

    @staticmethod
    async def request_codeforces():
        """ Request codeforces. """
        try:
            response = requests.get('https://codeforces.com/api/problemset.problems')
            data = response.json()

            if data['status'] == 'OK':
                results = data['result']
            else:
                results = None
            return results

        except requests.exceptions.RequestException as e:
            logging.error(f"Ошибка при получении данных: {e}")
            return None

        except Exception as e:
            logging.error(f"Неизвестная ошибка: {e}")
            return None

    @staticmethod
    async def get_tags_map():
        """ Get tags map. """
        try:
            tags_query = await Subject.all()
            tags_map = {tag.tag: tag for tag in tags_query}
            return tags_map
        except Exception as e:
            logging.error(f"Ошибка при получении данных из базы: {e}")
            return None

    @staticmethod
    async def process_tasks(problems, tags_map, problem_statistics):
        """ Process tasks. """
        for problem in problems:
            name = problem.get("name", "")
            number = f"{problem.get('contestId', 0)}{problem.get('index', '')}"
            rating = problem.get("rating")
            url = f"https://codeforces.com/problemset/problem/{problem.get('contestId')}/{problem.get('index')}"
            solved_count = problem_statistics.get(number, 0)

            tags = []

            for tag in problem.get("tags", []):
                subject = tags_map.get(tag)
                if subject:
                    tags.append(subject)

            # Create or update task
            task, created = await Task.get_or_create(number=number, defaults={
                "name": name,
                "rating": rating,
                "url": url,
                "solved_count": solved_count,
            })

            if not created:
                task.name = name
                task.rating = rating
                task.url = url
                task.solved_count = solved_count
                await task.save()

            await task.subject.clear()
            await task.subject.add(*tags)
