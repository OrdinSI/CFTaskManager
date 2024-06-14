class ChatView:
    """ Chat view. """

    def __init__(self, bot):
        self.bot = bot

    async def send_message(self, chat_id, message):
        """ Send message to chat. """
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="HTML"
            )
        except Exception as e:
            raise e

    async def send_message_with_keyboard(self, chat_id, message, reply_markup):
        """ Send message with keyboard. """
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        except Exception as e:
            raise e

    @staticmethod
    async def delete_message(message):
        """ Delete message. """
        try:
            await message.delete()
        except Exception as e:
            raise e

    @staticmethod
    async def edit_message_reply_markup(message, reply_markup):
        """ Edit message reply markup """
        try:
            if message:
                await message.edit_reply_markup(
                    reply_markup=reply_markup
                )
        except Exception as e:
            raise e

    @staticmethod
    async def answer_callback_query(callback_query, text: str = None, show_alert: bool = False):
        """ Answer callback query """
        try:
            await callback_query.answer(
                text=text,
                show_alert=show_alert
            )
        except Exception as e:
            raise e

    async def edit_message_with_keyboard(self, chat_id, message_id, new_message, reply_markup):
        """ Edit existing message with new text and keyboard. """
        try:
            await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_message,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
        except Exception as e:
            raise e
