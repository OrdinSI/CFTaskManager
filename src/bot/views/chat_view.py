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
