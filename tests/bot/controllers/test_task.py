import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.bot.controllers.task import TaskController, TaskState
from src.bot.messages import EXIT_MESSAGE, TAG_RATING_MESSAGE_KEYBOARD, TASK_INFO, \
    TASK_MESSAGE_KEYBOARD


@pytest.fixture
def task_controller():
    chat_view = AsyncMock()
    task_keyboard = AsyncMock()
    task_model = AsyncMock()
    return TaskController(chat_view=chat_view, task_model=task_model, task_keyboard=task_keyboard)


@pytest.mark.asyncio
async def test_cmd_task(task_controller):
    message = AsyncMock(spec=Message)
    state = AsyncMock(spec=FSMContext)
    message.from_user = MagicMock()
    message.from_user.id = 12345

    task_controller.task_model.get_subjects.return_value = ["Math", "Physics"]
    task_controller.task_keyboard.keyboard_subjects.return_value = "keyboard_stub"

    with patch("logging.error") as mock_logging_error:
        await task_controller.cmd_task(message, state)

        state.set_state.assert_called_once_with(TaskState.subject)
        state.update_data.assert_called_once_with(subjects=["Math", "Physics"])
        task_controller.chat_view.send_message_with_keyboard.assert_called_once_with(
            12345, TAG_RATING_MESSAGE_KEYBOARD, reply_markup="keyboard_stub"
        )
        mock_logging_error.assert_not_called()


@pytest.mark.asyncio
async def test_handle_callback_subject(task_controller):
    callback_query = AsyncMock(spec=CallbackQuery)
    state = AsyncMock(spec=FSMContext)
    callback_query.data = "page_1"
    callback_query.message = MagicMock()

    state.get_data.return_value = {
        "subjects": ["Math", "Physics"]
    }
    task_controller.task_keyboard.keyboard_subjects.return_value = "keyboard_stub"

    with patch("logging.error") as mock_logging_error:
        await task_controller.handle_callback_subject(callback_query, state)

        task_controller.chat_view.edit_message_reply_markup.assert_called_once_with(
            callback_query.message, reply_markup="keyboard_stub"
        )
        task_controller.chat_view.answer_callback_query.assert_called_once_with(callback_query)
        mock_logging_error.assert_not_called()


@pytest.mark.asyncio
async def test_handle_callback_exit(task_controller):
    callback_query = AsyncMock(spec=CallbackQuery)
    state = AsyncMock(spec=FSMContext)
    callback_query.message = MagicMock()
    callback_query.from_user = MagicMock()
    callback_query.from_user.id = 12345

    with patch("logging.error") as mock_logging_error:
        await task_controller.handle_callback_exit(callback_query, state)

        state.clear.assert_called_once()
        task_controller.chat_view.delete_message.assert_called_once_with(callback_query.message)
        task_controller.chat_view.send_message.assert_called_once_with(12345, EXIT_MESSAGE)
        task_controller.chat_view.answer_callback_query.assert_called_once_with(callback_query)
        mock_logging_error.assert_not_called()


@pytest.mark.asyncio
async def test_handle_callback_rating(task_controller):
    callback_query = AsyncMock(spec=CallbackQuery)
    callback_query.data = "tag_Math"
    contest_mock = MagicMock()
    callback_query.message = MagicMock()
    contest_mock.name = "Math_1000"
    task_controller.task_model.get_contests_by_subject.return_value = [contest_mock]
    task_controller.task_keyboard.keyboard_ratings.return_value = "keyboard_stub"

    with patch("logging.error") as mock_logging_error:
        await task_controller.handle_callback_rating(callback_query)

        task_controller.chat_view.edit_message_reply_markup.assert_called_once_with(
            callback_query.message, reply_markup="keyboard_stub"
        )
        task_controller.chat_view.answer_callback_query.assert_called_once_with(callback_query)
        mock_logging_error.assert_not_called()


@pytest.mark.asyncio
async def test_handle_callback_task(task_controller):
    callback_query = AsyncMock(spec=CallbackQuery)
    state = AsyncMock(spec=FSMContext)
    callback_query.data = "task_Math_1000"
    callback_query.message = MagicMock()
    callback_query.message.chat.id = 12345
    callback_query.message.message_id = 54321

    task_mock = MagicMock()
    task_controller.task_model.get_tasks_by_tag_and_rating.return_value = [task_mock]
    task_controller.task_keyboard.keyboard_tasks.return_value = "keyboard_stub"

    with patch("logging.error") as mock_logging_error:
        await task_controller.handle_callback_task(callback_query, state)

        state.set_state.assert_called_once_with(TaskState.task)
        state.update_data.assert_called_once_with(tasks=[task_mock])
        task_controller.chat_view.edit_message_with_keyboard.assert_called_once_with(
            chat_id=12345,
            message_id=54321,
            new_message=TASK_MESSAGE_KEYBOARD,
            reply_markup="keyboard_stub"
        )
        task_controller.chat_view.answer_callback_query.assert_called_once_with(callback_query)
        mock_logging_error.assert_not_called()


@pytest.mark.asyncio
async def test_handle_callback_task_page(task_controller):
    callback_query = AsyncMock(spec=CallbackQuery)
    state = AsyncMock(spec=FSMContext)
    callback_query.message = MagicMock()
    callback_query.data = "tk_page_2"
    state.get_data.return_value = {
        "tasks": ["task1", "task2"]
    }

    task_controller.task_keyboard.keyboard_tasks.return_value = "keyboard_stub"

    with patch("logging.error") as mock_logging_error:
        await task_controller.handle_callback_task_page(callback_query, state)

        task_controller.chat_view.edit_message_reply_markup.assert_called_once_with(
            callback_query.message, reply_markup="keyboard_stub"
        )
        task_controller.chat_view.answer_callback_query.assert_called_once_with(callback_query)
        mock_logging_error.assert_not_called()


@pytest.mark.asyncio
async def test_handle_callback_task_info(task_controller):
    callback_query = AsyncMock(spec=CallbackQuery)
    state = AsyncMock(spec=FSMContext)
    callback_query.data = "id_1"
    callback_query.message = MagicMock()
    callback_query.from_user = MagicMock()
    callback_query.from_user.id = 12345

    task_mock = MagicMock()
    task_mock.id = 1
    task_mock.name = "Task 1"
    task_mock.rating = 1000
    task_mock.solved_count = 50
    task_mock.url = "http://example.com"

    state.get_data.return_value = {
        "tasks": [task_mock]
    }

    with patch("logging.error") as mock_logging_error:
        await task_controller.handle_callback_task_info(callback_query, state)

        task_controller.chat_view.delete_message.assert_called_once_with(callback_query.message)
        task_controller.chat_view.send_message.assert_called_once_with(
            12345,
            TASK_INFO.format("Task 1", 1000, 50, "http://example.com")
        )
        task_controller.chat_view.answer_callback_query.assert_called_once_with(callback_query)
        mock_logging_error.assert_not_called()
