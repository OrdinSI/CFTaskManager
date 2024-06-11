import asyncio
import logging
import signal
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tortoise import Tortoise

from src.parser.parser import Parser
from src.settings import TORTOISE_ORM

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(module)s:  [%(funcName)s] %(message)s'
)

logging.info(f'Starting app..')


async def run_db():
    try:
        logging.info('Starting database...')
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas(safe=True)
    except Exception as e:
        logging.error(e)


async def close_db():
    await Tortoise.close_connections()


def signal_handler(sig, frame):
    asyncio.ensure_future(close_db())
    asyncio.get_event_loop().stop()


async def start_scheduler():
    """ Start scheduler. """
    try:
        parser = Parser()
        scheduler = AsyncIOScheduler()
        scheduler.add_job(parser.parse, 'interval', seconds=10)
        scheduler.start()
    except Exception as e:
        logging.error(f"Ошибка при запуске задачи: {e}")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler, sig, None)

    try:
        loop.run_until_complete(run_db())
        loop.run_until_complete(start_scheduler())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(close_db())
        loop.close()
