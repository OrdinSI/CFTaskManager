import pytest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.views.task_keyboard import TaskKeyboard


class MockSubject:
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag


class MockTask:
    def __init__(self, name, task_id):
        self.name = name
        self.id = task_id


@pytest.mark.asyncio
async def test_keyboard_subjects():
    subjects = [MockSubject(name=f"Subject {i}", tag=f"tag{i}") for i in range(1, 21)]
    page = 1
    page_size = 10

    keyboard = await TaskKeyboard.keyboard_subjects(subjects, page, page_size)
    assert isinstance(keyboard, InlineKeyboardMarkup)
    assert len(keyboard.inline_keyboard) == 12

    first_button = keyboard.inline_keyboard[0][0]
    assert isinstance(first_button, InlineKeyboardButton)
    assert first_button.text == "Subject 1"
    assert first_button.callback_data == "tag_tag1"


@pytest.mark.asyncio
async def test_keyboard_ratings():
    ratings = ["A", "B", "C", "D", "E", "F", "G"]
    tag = "example_tag"

    keyboard = await TaskKeyboard.keyboard_ratings(ratings, tag)
    assert isinstance(keyboard, InlineKeyboardMarkup)
    assert len(keyboard.inline_keyboard) == 3

    first_button = keyboard.inline_keyboard[0][0]
    assert first_button.text == "A"
    assert first_button.callback_data == "task_example_tag_A"


@pytest.mark.asyncio
async def test_keyboard_tasks():
    tasks = [MockTask(name=f"Task {i}", task_id=i) for i in range(1, 21)]
    page = 1
    page_size = 10

    keyboard = await TaskKeyboard.keyboard_tasks(tasks, page, page_size)
    assert isinstance(keyboard, InlineKeyboardMarkup)
    assert len(keyboard.inline_keyboard) == 12

    first_button = keyboard.inline_keyboard[0][0]
    assert isinstance(first_button, InlineKeyboardButton)
    assert first_button.text == "Task 1"
    assert first_button.callback_data == "id_1"
