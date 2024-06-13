import logging

from apscheduler.events import (EVENT_JOB_ERROR, EVENT_JOB_EXECUTED,
                                EVENT_JOB_MISSED)
from apscheduler.schedulers.asyncio import AsyncIOScheduler


class ParserManager:
    """ Parser manager. """

    def __init__(self, parser):
        self.scheduler = None
        self.parser = parser

    @staticmethod
    def job_listener(event):
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
            self.scheduler = AsyncIOScheduler(job_defaults={'misfire_grace_time': 60})
            self.scheduler.add_job(self.parser.parse, 'interval', seconds=300)
            self.scheduler.add_listener(self.job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)
            self.scheduler.start()
            logging.info('Started task.')
            logging.info(f'Tasks: {self.scheduler.get_jobs()}')
        except Exception as e:
            logging.error(f"Error starting scheduler: {e}")

    async def shutdown(self):
        """ Shutdown scheduler. """
        if self.scheduler:
            logging.info("Scheduler shutting down...")
            await self.scheduler.shutdown(wait=False)
