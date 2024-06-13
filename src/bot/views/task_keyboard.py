from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class TaskKeyboard:
    """ Task keyboard. """

    def __init__(self):
        pass

    async def keyboard_subjects(self, subjects, page: int = 1, page_size: int = 10):
        """ Keyboard for subjects. """
        total_pages = (len(subjects) + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        subjects = subjects[start:end]

        buttons = []
        for subject in subjects:
            callback_data = f"tag_{subject.tag}" if subject.tag else "tag_empty"
            buttons.append([InlineKeyboardButton(text=subject.name, callback_data=callback_data)])

        navigation_buttons = []
        if page > 1:
            navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}"))
        if page < total_pages:
            navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page + 1}"))

        if navigation_buttons:
            buttons.append(navigation_buttons)

        buttons.append([InlineKeyboardButton(text="Выход", callback_data="exit_subjects")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    async def keyboard_ratings(self, ratings, tag):
        """ Keyboard for ratings. """

        buttons = []
        for i in range(0, len(ratings), 5):
            row_buttons = []
            for rating in ratings[i:i + 5]:
                callback_data = f"task_{tag}_{rating}"
                row_buttons.append(InlineKeyboardButton(text=rating, callback_data=callback_data))
            buttons.append(row_buttons)

        buttons.append([InlineKeyboardButton(text="Выход", callback_data="exit_subjects")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard

    async def keyboard_tasks(self, tasks, page: int = 1, page_size: int = 10):
        """ Keyboard for tasks"""
        total_pages = (len(tasks) + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size
        tasks = tasks[start:end]

        buttons = []
        for task in tasks:
            callback_data = f"id_{task.id}"
            buttons.append([InlineKeyboardButton(text=task.name, callback_data=callback_data)])

        navigation_buttons = []
        if page > 1:
            navigation_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"tk_page_{page - 1}"))
        if page < total_pages:
            navigation_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"tk_page_{page + 1}"))

        if navigation_buttons:
            buttons.append(navigation_buttons)

        buttons.append([InlineKeyboardButton(text="Выход", callback_data="exit_subjects")])

        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        return keyboard


