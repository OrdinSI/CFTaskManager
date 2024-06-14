import signal

import pytest
import asyncio
from unittest.mock import patch, AsyncMock
from main import AppManager


@pytest.fixture
def app_manager():
    return AppManager()


@pytest.mark.asyncio
async def test_shutdown(app_manager):
    with patch.object(app_manager.dp.storage, 'close', new_callable=AsyncMock), \
            patch.object(app_manager.bot_manager.bot.session, 'close', new_callable=AsyncMock), \
            patch.object(app_manager.db_manager, 'close_db', new_callable=AsyncMock), \
            patch.object(app_manager.scheduler_manager, 'shutdown', new_callable=AsyncMock):
        await app_manager.shutdown(signal.SIGINT)
        app_manager.dp.storage.close.assert_called_once()
        app_manager.bot_manager.bot.session.close.assert_called_once()
        app_manager.db_manager.close_db.assert_called_once()
        app_manager.scheduler_manager.shutdown.assert_called_once()


@pytest.mark.asyncio
async def test_setup_signals(app_manager):
    """ Тест для функции setup_signals. """
    loop = asyncio.get_event_loop()

    with patch.object(loop, 'add_signal_handler') as mock_add_signal_handler:
        app_manager.setup_signals(loop)

        assert mock_add_signal_handler.call_count == 2


if __name__ == "__main__":
    pytest.main()
