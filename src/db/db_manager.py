from src.settings import TORTOISE_ORM
from tortoise import Tortoise
import logging


class DBManager:
    """ DB manager. """

    def __init__(self):
        pass

    @staticmethod
    async def run_db():
        """ Run db. """
        try:
            logging.info('Starting db...')
            await Tortoise.init(config=TORTOISE_ORM)
            await Tortoise.generate_schemas(safe=True)
        except Exception as e:
            logging.error(e)

    @staticmethod
    async def close_db():
        """ Close db. """
        logging.info('Closing db...')
        await Tortoise.close_connections()
