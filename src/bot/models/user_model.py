from src.db.models.user import User


class UserModel:
    """ User model. """

    def __init__(self):
        pass

    @staticmethod
    async def get_user(user_id: int) -> User:
        """ Get user. """
        return await User.get_or_none(user_id=user_id)

    @staticmethod
    async def create_user(user_id: int, user_name: str) -> None:
        """ Create user. """
        user, created = await User.get_or_create(user_id=user_id, user_name=user_name)
        if not created:
            user.user_id = user_id
            user.user_name = user_name
            await user.save()
