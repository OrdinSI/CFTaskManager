import pytest
from unittest.mock import AsyncMock, patch

from src.bot.models.user_model import UserModel
from src.db.models.user import User
import tortoise.exceptions


@pytest.mark.asyncio
async def test_get_user():
    user_id = 1
    user_mock = AsyncMock(spec=User)

    with patch('src.db.models.user.User.get', AsyncMock(return_value=user_mock)) as mock_get:
        result = await UserModel.get_user(user_id)

        mock_get.assert_called_once_with(user_id=user_id)
        assert result == user_mock

    with patch('src.db.models.user.User.get', AsyncMock(side_effect=tortoise.exceptions.DoesNotExist)) as mock_get:
        result = await UserModel.get_user(user_id)

        mock_get.assert_called_once_with(user_id=user_id)
        assert result is None

    with patch('src.db.models.user.User.get', AsyncMock(side_effect=Exception("Some error"))) as mock_get:
        with pytest.raises(Exception, match="Some error"):
            await UserModel.get_user(user_id)

        mock_get.assert_called_once_with(user_id=user_id)


@pytest.mark.asyncio
async def test_create_user():
    user_id = 1
    user_name = "John Doe"
    user_mock = AsyncMock(spec=User)

    with patch('src.db.models.user.User.get_or_create',
               AsyncMock(return_value=(user_mock, True))) as mock_get_or_create:
        await UserModel.create_user(user_id, user_name)

        mock_get_or_create.assert_called_once_with(user_id=user_id, user_name=user_name)
        user_mock.save.assert_not_awaited()

    with patch('src.db.models.user.User.get_or_create',
               AsyncMock(return_value=(user_mock, False))) as mock_get_or_create:
        with patch.object(user_mock, 'save', new_callable=AsyncMock) as mock_save:
            await UserModel.create_user(user_id, user_name)

            mock_get_or_create.assert_called_once_with(user_id=user_id, user_name=user_name)
            mock_save.assert_awaited_once()

    with patch('src.db.models.user.User.get_or_create',
               AsyncMock(side_effect=Exception("Some error"))) as mock_get_or_create:
        with pytest.raises(Exception, match="Some error"):
            await UserModel.create_user(user_id, user_name)

        mock_get_or_create.assert_called_once_with(user_id=user_id, user_name=user_name)
