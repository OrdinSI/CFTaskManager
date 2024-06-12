from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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
            callback_data = f"tag_{str(subject.tag)}" if subject.tag else "tag_empty"
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
