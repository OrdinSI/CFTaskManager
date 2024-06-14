import pytest
from unittest.mock import AsyncMock, Mock

from src.bot.views.chat_view import ChatView


@pytest.fixture
def bot_mock():
    bot = Mock()
    bot.send_message = AsyncMock()
    bot.edit_message_text = AsyncMock()
    return bot


@pytest.fixture
def chat_view(bot_mock):
    return ChatView(bot=bot_mock)


@pytest.mark.asyncio
async def test_send_message(chat_view, bot_mock):
    chat_id = 123
    message = "Hello, world!"

    await chat_view.send_message(chat_id, message)

    bot_mock.send_message.assert_awaited_once_with(
        chat_id=chat_id,
        text=message,
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_send_message_with_keyboard(chat_view, bot_mock):
    chat_id = 123
    message = "Hello, world!"
    reply_markup = Mock()

    await chat_view.send_message_with_keyboard(chat_id, message, reply_markup)

    bot_mock.send_message.assert_awaited_once_with(
        chat_id=chat_id,
        text=message,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )


@pytest.mark.asyncio
async def test_delete_message():
    message_mock = Mock(delete=AsyncMock())

    await ChatView.delete_message(message_mock)

    message_mock.delete.assert_awaited_once()


@pytest.mark.asyncio
async def test_edit_message_reply_markup():
    message_mock = Mock(edit_reply_markup=AsyncMock())
    reply_markup = Mock()

    await ChatView.edit_message_reply_markup(message_mock, reply_markup)

    message_mock.edit_reply_markup.assert_awaited_once_with(
        reply_markup=reply_markup
    )


@pytest.mark.asyncio
async def test_answer_callback_query():
    callback_query_mock = Mock(answer=AsyncMock())
    text = "Callback response"

    await ChatView.answer_callback_query(callback_query_mock, text, show_alert=True)

    callback_query_mock.answer.assert_awaited_once_with(
        text=text,
        show_alert=True
    )


@pytest.mark.asyncio
async def test_edit_message_with_keyboard(chat_view, bot_mock):
    chat_id = 123
    message_id = 456
    new_message = "Updated message"
    reply_markup = Mock()

    await chat_view.edit_message_with_keyboard(chat_id, message_id, new_message, reply_markup)

    bot_mock.edit_message_text.assert_awaited_once_with(
        chat_id=chat_id,
        message_id=message_id,
        text=new_message,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
