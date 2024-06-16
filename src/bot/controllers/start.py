import logging

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
        try:
            user_id = message.from_user.id
            user_name = message.from_user.username if message.from_user.username else "Пользователь"

            user = await self.start_model.get_user(user_id)
            if user is None:
                await self.start_model.create_user(user_id, user_name)

            await self.chat_view.send_message(user_id, NEW_USER_GREETING.format(user_name))
        except Exception as e:
            logging.error(f"Ошибка при выполнении команды start: {e}", exc_info=True)
