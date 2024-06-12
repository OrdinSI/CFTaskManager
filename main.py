import asyncio
import logging
import signal
import sys

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from tortoise import Tortoise

from src.parser.parser import Parser
from src.settings import TORTOISE_ORM


class AppManager:
    """ App manager. """
    def __init__(self):
        self.scheduler = None

    def setup_signals(self, loop):
        """ Setup signals. """
        loop.add_signal_handler(signal.SIGINT, lambda: asyncio.create_task(self.shutdown(signal.SIGINT)))
        loop.add_signal_handler(signal.SIGTERM, lambda: asyncio.create_task(self.shutdown(signal.SIGTERM)))

    async def run_db(self):
        """ Run db. """
        try:
            logging.info('Starting db...')
            await Tortoise.init(config=TORTOISE_ORM)
            await Tortoise.generate_schemas(safe=True)
        except Exception as e:
            logging.error(e)

    async def close_db(self):
        logging.info('Closing db...')
        await Tortoise.close_connections()

    async def shutdown(self, sig):
        """ Shutdown. """
        logging.info(f"Stopping signal {sig.name}...")
        if self.scheduler:
            logging.info("Scheduler shutting down...")
            self.scheduler.shutdown(wait=False)
        await self.close_db()
        asyncio.get_event_loop().stop()

    def job_listener(self, event):
        """ Job listener. """
        if event.code == EVENT_JOB_EXECUTED:
            logging.info(f'Job {event.job_id} executed successfully at {event.scheduled_run_time}')
        elif event.code == EVENT_JOB_ERROR:
            logging.error(f'Job {event.job_id} failed with exception: {event.exception}')
            logging.error(f'Traceback: {event.traceback}')
        elif event.code == EVENT_JOB_MISSED:
            logging.warning(f'Job {event.job_id} missed at {event.scheduled_run_time}')

    async def start_scheduler(self):
        """ Start scheduler. """
        try:
            parser = Parser()
            self.scheduler = AsyncIOScheduler(job_defaults={'misfire_grace_time': 60})
            self.scheduler.add_job(parser.parse, 'interval', seconds=300)
            self.scheduler.add_listener(self.job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
            self.scheduler.start()
            logging.info('Started task.')
            logging.info(f'Tasks: {self.scheduler.get_jobs()}')
        except Exception as e:
            logging.error(f"Error starting scheduler: {e}")

    async def start_bot(self):
        """ Start bot. """
        # Здесь будет код для старта бота
        logging.info('Starting bot...')
        await asyncio.sleep(1)


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
        loop.run_until_complete(app_manager.run_db())
        loop.run_until_complete(app_manager.start_scheduler())
        loop.run_until_complete(app_manager.start_bot())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(app_manager.close_db())
        loop.close()
