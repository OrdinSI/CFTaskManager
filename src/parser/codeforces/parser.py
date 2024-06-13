import logging

import aiohttp

from src.db.models.task import Contest, Subject, Task
from src.parser.utils.utils import get_fresh_cookies_and_headers


class Parser:
    """ Class for parsing. """

    def __init__(self):
        self.base_url = "https://codeforces.com/api/"

    async def parse(self):
        """ Main method. """
        logging.info("Запуск парсинга.")
        try:
            results = await self.request_codeforces()

            if not results:
                return

            problems = results["problems"]
            problem_statistics = {f"{stat['contestId']}{stat['index']}": stat['solvedCount'] for stat in
                                  results["problemStatistics"]}

            logging.info(f"Всего задач: {len(problems)}")

            tags_map = await self.get_tags_map()
            logging.info(f"Всего тегов: {len(tags_map)}")
            await self.process_tasks(problems, tags_map, problem_statistics)

        except Exception as e:
            logging.error(f"Ошибка при парсинге: {e}")

    async def request_codeforces(self):
        """ Request codeforces. """
        # День все было нормально запросы уходили раз в час.
        # После чего блокнуло и возвращало 403.
        # Ответа не было даже с апи ключом, странное у них апи.
        # Пришлось использовать selenium.
        url = f"{self.base_url}problemset.problems?lang=ru"

        cookies, headers = get_fresh_cookies_and_headers(self.base_url)
        logging.info("Получение свежих cookies и заголовков.")
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
        logging.info("Получение данных из базы.")
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

        logging.info("Запуск обработки задач.")
        for problem in problems:
            try:
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

                if not first_tag or not tags:
                    first_tag = ""
                    tags = [tags_map[""]]

                # Create contest
                contest_name = f"{first_tag}_{rating}_{number}"
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

            except Exception as e:
                logging.error(f"Ошибка при обработке задачи {problem.get('contestId')} {problem.get('index')}: {e}")
                continue
