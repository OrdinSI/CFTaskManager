from aiogram import Router, types
from aiogram.filters import CommandStart

from src.bot.messages import NEW_USER_GREETING


class StartController:
    """ Controller for start command. """
    def __init__(self, chat_view, start_model):
        self.start_model = start_model
        self.chat_view = chat_view
        self.router = Router()
        self.router.message.register(self.cmd_start, CommandStart())

    async def cmd_start(self, message: types.Message):
        """ Start command. """
        chat_id = message.chat.id
        user_name = message.from_user.username if message.from_user.username else "Пользователь"

        user = await self.start_model.get_user(chat_id)
        if not user:
            await self.start_model.create_user(chat_id, user_name)

        await self.chat_view.send_message(chat_id, NEW_USER_GREETING.format(user_name))



