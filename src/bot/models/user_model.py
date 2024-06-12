from src.db.models.user import User


class UserModel:
    """ User model. """

    def __init__(self):
        pass

    async def get_user(self, user_id):
        """ Get user. """
        return await User.get_or_none(user_id=user_id)

    async def create_user(self, user_id, user_name):
        """ Create user. """
        user, created = await User.get_or_create(user_id=user_id, user_name=user_name)
        if not created:
            user.user_id = user_id
            user.user_name = user_name
            await user.save()

