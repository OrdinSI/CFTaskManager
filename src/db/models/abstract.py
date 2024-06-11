from tortoise import fields
from tortoise.models import Model


class AbstractBaseModel(Model):
    """
    Abstract base model for Tortoise ORM.

    :param id: primary key
    :param created_at: creation date
    :param updated_at: update date
    """
    id = fields.BigIntField(primary_key=True)
    created_at = fields.DatetimeField(auto_now_add=True, null=True)
    updated_at = fields.DatetimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
