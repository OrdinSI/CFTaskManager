import pytest
from unittest.mock import patch, AsyncMock, create_autospec
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.bot.bot_manager import BotManager
from src.settings import BOT_TOKEN


@pytest.fixture
def bot_manager():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    return BotManager(bot, dp)


@pytest.mark.asyncio
async def test_start_bot(bot_manager):
    with patch.object(bot_manager.dp, 'start_polling', new_callable=AsyncMock):
        await bot_manager.start_bot()
        bot_manager.dp.start_polling.assert_called_once()
