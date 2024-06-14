import pytest
from unittest.mock import AsyncMock, patch

from src.bot.models.user_model import UserModel
from src.db.models.user import User


@pytest.mark.asyncio
async def test_get_user():
    user_id = 1
    user_mock = AsyncMock(spec=User)

    with patch('src.db.models.user.User.get_or_none', AsyncMock(return_value=user_mock)) as mock_get_or_none:
        result = await UserModel.get_user(user_id)

        mock_get_or_none.assert_called_once_with(user_id=user_id)
        assert result == user_mock


@pytest.mark.asyncio
async def test_create_user():
    user_id = 1
    user_name = "John Doe"
    user_mock = AsyncMock(spec=User)

    with patch('src.db.models.user.User.get_or_create', new_callable=AsyncMock) as mock_get_or_create:
        mock_get_or_create.return_value = (user_mock, False)

        with patch.object(user_mock, 'save', new_callable=AsyncMock) as mock_save:
            await UserModel.create_user(user_id, user_name)

            mock_get_or_create.assert_called_once_with(user_id=user_id, user_name=user_name)
            mock_save.assert_awaited_once()

