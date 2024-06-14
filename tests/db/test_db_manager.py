import pytest
import logging
from tortoise import Tortoise
from src.db.db_manager import DBManager


TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://:memory:"
    },
    "apps": {
        "models": {
            "models": ["src.db.models.task", "src.db.models.user", "aerich.models"],
            "default_connection": "default",
        }
    }
}


@pytest.fixture(scope="module", autouse=True)
async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    yield
    await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_run_db(caplog):
    caplog.set_level(logging.INFO)

    await DBManager.run_db()

    assert "Starting db..." in caplog.text


@pytest.mark.asyncio
async def test_close_db(caplog):
    caplog.set_level(logging.INFO)

    await DBManager.close_db()

    assert "Closing db..." in caplog.text
