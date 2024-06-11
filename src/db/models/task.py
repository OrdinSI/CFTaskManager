from tortoise import fields

from src.db.models.abstract import AbstractBaseModel


class Subject(AbstractBaseModel):
    """
    Model for task subjects (tags)

    :param tag: тег
    :param name: название темы
    """
    tag = fields.CharField(30, unique=True)
    name = fields.CharField(100, unique=True)

    class Meta:
        table = "subjects"

    def __str__(self):
        return self.name


class Task(AbstractBaseModel):
    """
    Model for tasks

    :param name: название задачи
    :param number: номер задачи
    :param subject: тема
    :param solved_count: количество решивших задачу
    :param rating: рейтинг задачи

    """
    name = fields.CharField(100)
    number = fields.CharField(30, unique=True, null=True)
    subject = fields.ManyToManyField("models.Subject", related_name="tasks")
    solved_count = fields.BigIntField(default=0)
    rating = fields.BigIntField(default=0)
    url = fields.CharField(150)
    used_in_contest = fields.BooleanField(default=False)

    class Meta:
        table = "tasks"

    def __str__(self):
        return self.name
