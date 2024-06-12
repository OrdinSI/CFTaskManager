import logging

from aiogram import Router, types
from aiogram.filters import Command

from src.bot.messages import TASKS_MESSAGE_KEYBOARD, EXIT_MESSAGE


class TaskController:
    """ Controller for tasks command. """

    def __init__(self, chat_view, tasks_model, task_keyboard):
        self.chat_view = chat_view
        self.tasks_model = tasks_model
        self.task_keyboard = task_keyboard
        self.router = Router()

        self.router.message.register(self.cmd_task, Command("tasks"))
        self.router.callback_query.register(self.handle_callback_subject, lambda x: x.data.startswith("page_"))
        self.router.callback_query.register(self.handle_callback_exit, lambda x: x.data == "exit_subjects")

    async def cmd_task(self, message: types.Message):
        """ Command for tasks. """
        user_id = message.from_user.id
        subjects = await self.tasks_model.get_subjects()
        keyboard = await self.task_keyboard.keyboard_subjects(subjects, page=1)
        await self.chat_view.send_message_with_keyboard(user_id, TASKS_MESSAGE_KEYBOARD, reply_markup=keyboard)

    async def handle_callback_subject(self, callback_query: types.CallbackQuery):
        """ Handle callback for subject. """
        data = callback_query.data

        page_number = int(data.split("_")[1])
        subjects = await self.tasks_model.get_subjects()
        keyboard = await self.task_keyboard.keyboard_subjects(subjects, page=page_number)
        await self.chat_view.edit_message_reply_markup(callback_query.message, reply_markup=keyboard)
        await self.chat_view.answer_callback_query(callback_query)

    async def handle_callback_exit(self, callback_query: types.CallbackQuery):
        """ Handle callback for exit. """
        user_id = callback_query.from_user.id
        await self.chat_view.delete_message(callback_query.message)
        await self.chat_view.send_message(user_id, EXIT_MESSAGE)
        await self.chat_view.answer_callback_query(callback_query)
