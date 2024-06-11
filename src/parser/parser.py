import logging

import aiohttp

from src.db.models.task import Contest, Subject, Task
from src.settings import cookies, headers


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
        url = "https://codeforces.com/api/problemset.problems"
        # День все было нормально запросы уходили раз в час
        # После чего блокнуло и возвращало 403
        # Ответа не было даже с апи ключом решил к запросу добавить куки и хедеры из браузера
        # Странное у них апи
        async with aiohttp.ClientSession(headers=headers, cookies=cookies) as session:
            try:
                async with session.get(url) as response:
                    if response.status != 200:
                        logging.error(f"Ошибка HTTP: {response.status}, причина: {response.reason}")
                        return None

                    data = await response.json()

                    if data['status'] == 'OK':
                        results = data['result']
                        return results
                    else:
                        logging.error(f"Статус ответа не OK, получено: {data.get('status')}")
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
            rating = problem.get("rating", 0)
            url = f"https://codeforces.com/problemset/problem/{problem.get('contestId')}/{problem.get('index')}"
            solved_count = problem_statistics.get(number, 0)

            tags = []
            first_tag = None

            # Берем первый тег
            for idx, tag in enumerate(problem.get("tags", [])):
                if idx == 0:
                    first_tag = tag
                subject = tags_map.get(tag)
                if subject:
                    tags.append(subject)

            if not first_tag:
                logging.warning(f"Problem {number} пропущен потому что отсутствуют теги.")
                continue

            # Create contest
            contest_name = f"{first_tag}_{rating}"
            contest, created = await Contest.get_or_create(name=contest_name, subject=tags_map[first_tag])

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

            await contest.tasks.add(task)
