import logging


class ChatView:
    """ Chat view. """

    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, chat_id, message):
        """ Send message to chat. """
        try:
            await self.bot.send_message(chat_id=chat_id, text=message, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения, пользователь: {chat_id}, ошибка: {e}")

    async def send_message_with_keyboard(self, chat_id, message, reply_markup):
        """ Send message with keyboard. """
        try:
            await self.bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup, parse_mode="HTML")
        except Exception as e:
            logging.error(f"Ошибка при отправке сообщения, пользователь: {chat_id}, ошибка: {e}")

    async def delete_message(self, message):
        """ Delete message. """
        try:
            await message.delete()
        except Exception as e:
            logging.error(f"Ошибка при удалении сообщения: {e}")

    async def edit_message_reply_markup(self, message, reply_markup):
        """ Edit message reply markup """
        try:
            if message:
                await message.edit_reply_markup(reply_markup=reply_markup)
        except Exception as e:
            logging.error(f"Ошибка при обновлении клавиатуры сообщения: {e}")

    async def answer_callback_query(self, callback_query, text: str = None, show_alert: bool = False):
        """ Answer callback query """
        try:
            await callback_query.answer(text=text, show_alert=show_alert)
        except Exception as e:
            logging.error(f"Ошибка при ответе на коллбек-запрос: {e}")
