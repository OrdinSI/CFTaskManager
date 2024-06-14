import pytest
from unittest.mock import patch, AsyncMock

from src.bot.models.task_model import TaskModel
from src.db.models.task import Contest, Subject


@pytest.mark.asyncio
async def test_get_contests_by_subject():
    tag = "math"

    contests_mock = [AsyncMock(spec=Contest), AsyncMock(spec=Contest)]

    mock_filter = AsyncMock()
    mock_filter.all.return_value = contests_mock

    with patch('src.db.models.task.Contest.filter', return_value=mock_filter):
        result = await TaskModel.get_contests_by_subject(tag)

        mock_filter.all.assert_called_once()
        assert result == contests_mock


@pytest.mark.asyncio
async def test_get_subjects():
    subjects_mock = [AsyncMock(spec=Subject), AsyncMock(spec=Subject)]

    with patch('src.db.models.task.Subject.all', new_callable=AsyncMock) as mock_all:
        mock_all.return_value = subjects_mock

        result = await TaskModel.get_subjects()

        mock_all.assert_called_once()
        assert result == subjects_mock


@pytest.mark.asyncio
async def test_get_tasks_by_tag_and_rating():
    tag = "math"
    rating = 1000
    pattern = f"{tag}_{rating}_"

    tasks_mock = [AsyncMock(), AsyncMock()]
    contest_mock = AsyncMock(spec=Contest)
    contest_mock.tasks = AsyncMock()
    contest_mock.tasks.all = AsyncMock(return_value=tasks_mock)  # Соединяем AsyncMock с ответом
    contests_mock = [contest_mock, contest_mock]

    with patch('src.db.models.task.Contest.filter', return_value=AsyncMock()) as mock_filter:
        mock_filter.return_value.prefetch_related.return_value = contests_mock
        result = await TaskModel.get_tasks_by_tag_and_rating(tag, rating)

        mock_filter.assert_called_once_with(name__icontains=pattern)
        assert result == tasks_mock * 2
