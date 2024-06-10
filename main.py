import asyncio
import signal
from tortoise import Tortoise
from src.settings import TORTOISE_ORM


async def run_db():
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas()
    except Exception as e:
        print(e)


async def close_db():
    await Tortoise.close_connections()


def signal_handler(sig, frame):
    asyncio.ensure_future(close_db())
    asyncio.get_event_loop().stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, signal_handler, sig, None)

    try:
        loop.run_until_complete(run_db())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(close_db())
        loop.close()
