import asyncio
import logging
import signal
import sys
import platform

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.bot_manager import BotManager
from src.db.db_manager import DBManager
from src.parser.codeforces.parser import Parser
from src.parser.parser_manager import ParserManager
from src.settings import BOT_TOKEN


class AppManager:
    """ App manager. """

    def __init__(self):
        self.db_manager = DBManager()
        self.parser = Parser()
        self.scheduler_manager = ParserManager(self.parser)
        self.bot = Bot(token=BOT_TOKEN)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.bot_manager = BotManager(self.bot, self.dp)

    def setup_signals(self, loop):
        """ Setup signals. """
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.shutdown(signal.SIGINT)))
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.shutdown(signal.SIGTERM)))

    async def shutdown(self, sig):
        """ Shutdown. """
        logging.info(f"Stopping signal {sig.name}...")
        if self.scheduler_manager:
            logging.info("Scheduler shutting down...")
            await self.scheduler_manager.shutdown()
        await self.dp.storage.close()
        await self.bot.session.close()
        await self.db_manager.close_db()
        asyncio.get_event_loop().stop()


if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(module)s:  [%(funcName)s] %(message)s'
    )
    logging.info(f'Starting app..')

    loop = asyncio.get_event_loop()
    app_manager = AppManager()

    app_manager.setup_signals(loop)

    try:
        loop.run_until_complete(app_manager.db_manager.run_db())
        loop.run_until_complete(app_manager.scheduler_manager.start_scheduler())
        loop.run_until_complete(app_manager.bot_manager.start_bot())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(app_manager.db_manager.close_db())
        loop.close()
