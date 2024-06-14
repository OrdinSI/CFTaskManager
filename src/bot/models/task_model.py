from typing import List

from src.db.models.task import Contest, Subject


class TaskModel:
    """ Task model. """

    def __init__(self):
        pass

    @staticmethod
    async def get_contests_by_subject(tag: str) -> List[Contest]:
        """ Get tasks. """
        try:
            return await Contest.filter(subject__tag=tag).all()
        except Exception as e:
            raise e

    @staticmethod
    async def get_subjects() -> List[Subject]:
        """ Get subjects. """
        try:
            return await Subject.all()
        except Exception as e:
            raise e

    @staticmethod
    async def get_tasks_by_tag_and_rating(tag: str, rating: str) -> List[Contest]:
        """ Get tasks. """
        try:
            pattern = f"{tag}_{rating}_"
            contests = await Contest.filter(name__icontains=pattern).prefetch_related("tasks")

            tasks = []
            for contest in contests:
                tasks.extend(await contest.tasks.all())

            return tasks
        except Exception as e:
            raise e
