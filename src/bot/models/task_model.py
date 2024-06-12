from src.db.models.task import Contest, Subject


class TaskModel:
    """ Task model. """
    def __init__(self):
        pass

    async def get_tasks(self):
        """ Get tasks. """
        tasks = await Contest.all()
        return tasks

    async def get_subjects(self):
        """ Get subjects. """
        subjects = await Subject.all()
        return subjects
