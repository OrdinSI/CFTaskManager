import pytest
from unittest.mock import AsyncMock, patch

from src.db.db_manager import DBManager
from src.settings import TORTOISE_ORM


@pytest.fixture
def db_manager():
    return DBManager()


@pytest.mark.asyncio
async def test_run_db(db_manager):
    with patch('src.db.db_manager.Tortoise.init', new_callable=AsyncMock) as mock_init, \
            patch('src.db.db_manager.Tortoise.generate_schemas', new_callable=AsyncMock) as mock_generate_schemas:
        await db_manager.run_db()

        mock_init.assert_called_once_with(config=TORTOISE_ORM)
        mock_generate_schemas.assert_called_once_with(safe=True)


@pytest.mark.asyncio
async def test_close_db(db_manager):
    with patch('src.db.db_manager.Tortoise.close_connections', new_callable=AsyncMock) as mock_close_connections:
        await db_manager.close_db()
        mock_close_connections.assert_called_once()
