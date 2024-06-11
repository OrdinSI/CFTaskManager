from tortoise import fields

from src.db.models.abstract import AbstractBaseModel
from src.db.models.task import Task


class Contest(AbstractBaseModel):
    """
    Model for contests

    :param name: название контеста Тема + Сложность
    :param subject: основная тема контеста

    """
    name = fields.CharField(255, unique=True)
    subject = fields.ForeignKeyField("models.Subject", related_name="contests", on_delete=fields.CASCADE)
    tasks = fields.ManyToManyField("models.Task", related_name="contests")

    class Meta:
        table = "contests"

    def __str__(self):
        return self.name

    @classmethod
    async def create_contest(cls, name, subject):
        """
        Метод создает новый контест с заданными параметрами и добавляет задачи
        """
        contest = await cls.create(name=name, subject=subject)
        await contest.add_tasks()
        return contest

    async def add_tasks(self):
        """
        Метод добавляет задачи в контест
        """
        tasks_query = Task.filter(subjects__id=self.subject.id, used_in_contest=False)

        tasks = await tasks_query.all()

        for task in tasks:
            task.used_in_contest = True
            await task.save()

        await self.tasks.add(*tasks)
