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

    class Meta:
        table = "tasks"

    def __str__(self):
        return self.name


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
