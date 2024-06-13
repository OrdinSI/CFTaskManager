import datetime

import pytest
from unittest.mock import AsyncMock
from aiogram.types import Message, User as TelegramUser, Chat
from src.bot.controllers.start import StartController
from src.bot.messages import NEW_USER_GREETING
from src.db.models.user import User


@pytest.fixture
def start_controller():
    """ Фикстура для создания экземпляра StartController. """
    chat_view = AsyncMock()
    start_model = AsyncMock()
    return StartController(chat_view=chat_view, start_model=start_model)


@pytest.fixture
def mock_message():
    """ Фикстура для создания мок-объекта сообщения. """
    user = TelegramUser(id=123456, is_bot=False, first_name="Test", username="testuser")
    chat = Chat(id=123456, type="private", title="Test Chat")
    msg = Message(message_id=1, from_user=user, chat=chat, date=datetime.datetime.now(), text="/start")
    return msg


@pytest.mark.asyncio
async def test_cmd_start_new_user(start_controller, mock_message):
    """ Тест выполнения команды /start для нового пользователя. """
    start_controller.start_model.get_user.return_value = None
    await start_controller.cmd_start(mock_message)

    start_controller.start_model.get_user.assert_called_once_with(123456)
    start_controller.start_model.create_user.assert_called_once_with(123456, "testuser")
    start_controller.chat_view.send_message.assert_called_once_with(123456, NEW_USER_GREETING.format("testuser"))


@pytest.mark.asyncio
async def test_cmd_start_existing_user(start_controller, mock_message):
    """ Тест выполнения команды /start для существующего пользователя. """
    existing_user = User(user_id=123456, user_name="testuser")
    start_controller.start_model.get_user.return_value = existing_user
    await start_controller.cmd_start(mock_message)

    start_controller.start_model.get_user.assert_called_once_with(123456)
    start_controller.start_model.create_user.assert_not_called()
    start_controller.chat_view.send_message.assert_called_once_with(123456, NEW_USER_GREETING.format("testuser"))
