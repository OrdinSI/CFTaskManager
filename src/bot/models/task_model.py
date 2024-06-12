from src.db.models.task import Contest, Subject


class TaskModel:
    """ Task model. """
    def __init__(self):
        pass

    async def get_contests(self):
        """ Get tasks. """
        return await Contest.all()

    async def get_subjects(self):
        """ Get subjects. """
        return await Subject.all()
