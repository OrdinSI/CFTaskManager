import asyncio
import logging

import aiohttp
from aiogram import exceptions

from src.bot.controllers.start import StartController
from src.bot.controllers.task import TaskController
from src.bot.models.task_model import TaskModel
from src.bot.models.user_model import UserModel
from src.bot.views.chat_view import ChatView
from src.bot.views.task_keyboard import TaskKeyboard


class BotManager:
    """ Bot manager. """

    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp

        self.chat_view = ChatView(self.bot)
        self.start_model = UserModel()
        self.tasks_model = TaskModel()
        self.task_keyboard = TaskKeyboard()
        self.start_controller = StartController(self.chat_view, self.start_model)
        self.task_controller = TaskController(self.chat_view, self.tasks_model, self.task_keyboard)

        self.dp.include_router(self.start_controller.router)
        self.dp.include_router(self.task_controller.router)

    async def start_bot(self):
        """ Start bot. """
        logging.info('Starting bot...')
        while True:
            try:
                await self.dp.start_polling(self.bot)
                break
            except (aiohttp.ClientConnectorError, exceptions.TelegramAPIError) as e:
                logging.error(f"Error connecting to Telegram API: {e}")
                await asyncio.sleep(5)
            except Exception as e:
                logging.error(f"Error starting bot: {e}")
                await asyncio.sleep(5)
