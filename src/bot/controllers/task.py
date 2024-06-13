import logging

from aiogram.filters.state import State, StatesGroup
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from src.bot.messages import EXIT_MESSAGE, TAG_RATING_MESSAGE_KEYBOARD, TASK_MESSAGE_KEYBOARD


class TaskState(StatesGroup):
    """ Task states. """
    subject = State()
    task = State()


class TaskController:
    """ Controller for tasks command. """

    def __init__(self, chat_view, tasks_model, task_keyboard):
        self.chat_view = chat_view
        self.tasks_model = tasks_model
        self.task_keyboard = task_keyboard
        self.router = Router()

        self.router.message.register(self.cmd_task, Command("tasks"))
        self.router.callback_query.register(
            self.handle_callback_subject, lambda x: x.data.startswith("page_"), TaskState.subject)
        self.router.callback_query.register(self.handle_callback_exit, lambda x: x.data == "exit_subjects")
        self.router.callback_query.register(self.handle_callback_rating, lambda x: x.data.startswith("tag_"))
        self.router.callback_query.register(self.handle_callback_task, lambda x: x.data.startswith("task_"))
        self.router.callback_query.register(
            self.handle_callback_task_page, lambda x: x.data.startswith("tk_page_"), TaskState.task)

    async def cmd_task(self, message: types.Message, state: FSMContext):
        """ Command for tasks. """
        try:
            await state.set_state(TaskState.subject)
            user_id = message.from_user.id
            subjects = await self.tasks_model.get_subjects()
            await state.update_data(subjects=subjects)
            keyboard = await self.task_keyboard.keyboard_subjects(subjects, page=1)
            await self.chat_view.send_message_with_keyboard(user_id, TAG_RATING_MESSAGE_KEYBOARD, reply_markup=keyboard)
        except Exception as e:
            logging.error(f"Ошибка при выполнении команды tasks: {e}", exc_info=True)

    async def handle_callback_subject(self, callback_query: types.CallbackQuery, state: FSMContext):
        """ Handle callback for subject. """
        try:
            data = callback_query.data
            page_number = int(data.split("_")[1])
            state_data = await state.get_data()
            subjects = state_data.get("subjects", [])

            keyboard = await self.task_keyboard.keyboard_subjects(subjects, page=page_number)
            await self.chat_view.edit_message_reply_markup(callback_query.message, reply_markup=keyboard)
            await self.chat_view.answer_callback_query(callback_query)
        except Exception as e:
            logging.error(f"Ошибка при обработке handle_callback_subject: {e}", exc_info=True)

    async def handle_callback_exit(self, callback_query: types.CallbackQuery, state: FSMContext):
        """ Handle callback for exit. """
        try:
            await state.clear()
            user_id = callback_query.from_user.id
            await self.chat_view.delete_message(callback_query.message)
            await self.chat_view.send_message(user_id, EXIT_MESSAGE)
            await self.chat_view.answer_callback_query(callback_query)
        except Exception as e:
            logging.error(f"Ошибка при обработке handle_callback_exit: {e}", exc_info=True)

    async def handle_callback_rating(self, callback_query: types.CallbackQuery):
        """ Handle callback for rating. """
        try:
            data = callback_query.data
            tag = data.split("_")[1]
            if tag == "empty":
                tag = ""

            contests = await self.tasks_model.get_contests_by_subject(tag)
            ratings = list(
                set(int(contest.name.split("_")[1]) for contest in contests if contest.name.split("_")[0] == tag)
            )
            ratings.sort()

            ratings_str = [str(rating) for rating in ratings]

            keyboard = await self.task_keyboard.keyboard_ratings(ratings_str, tag)
            await self.chat_view.edit_message_reply_markup(callback_query.message, reply_markup=keyboard)
            await self.chat_view.answer_callback_query(callback_query)
        except Exception as e:
            logging.error(f"Ошибка при обработке handle_callback_rating: {e}", exc_info=True)

    async def handle_callback_task(self, callback_query: types.CallbackQuery, state: FSMContext):
        """ Handle callback for task. """
        try:
            await state.clear()
            await state.set_state(TaskState.task)
            data = callback_query.data
            tag = data.split("_")[1]
            rating = data.split("_")[2]

            tasks = await self.tasks_model.get_tasks_by_tag_and_rating(tag, rating)
            await state.update_data(tasks=tasks)

            keyboard = await self.task_keyboard.keyboard_tasks(tasks)
            await self.chat_view.edit_message_with_keyboard(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                new_message=TASK_MESSAGE_KEYBOARD,
                reply_markup=keyboard)
            await self.chat_view.answer_callback_query(callback_query)
        except Exception as e:
            logging.error(f"Ошибка при обработке handle_callback_task: {e}", exc_info=True)

    async def handle_callback_task_page(self, callback_query: types.CallbackQuery, state: FSMContext):
        """ Handle callback for task page. """
        try:
            data = callback_query.data
            page = int(data.split("_")[2])
            state_data = await state.get_data()
            tasks = state_data.get("tasks", [])

            keyboard = await self.task_keyboard.keyboard_tasks(tasks, page=page)
            await self.chat_view.edit_message_reply_markup(callback_query.message, reply_markup=keyboard)
            await self.chat_view.answer_callback_query(callback_query)
        except Exception as e:
            logging.error(f"Ошибка при обработке handle_callback_task_page: {e}", exc_info=True)
