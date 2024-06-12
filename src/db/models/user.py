from tortoise import fields

from src.db.models.abstract import AbstractBaseModel


class User(AbstractBaseModel):
    """
    User model.

    :param user_id: user id
    :param user_name: username
    """
    user_id = fields.BigIntField(unique=True)
    user_name = fields.CharField(255, default="")

    class Meta:
        table = "users"

    def __str__(self):
        return self.user_id
