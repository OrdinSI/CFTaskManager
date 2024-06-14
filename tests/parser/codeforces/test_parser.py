import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from aiohttp import ClientSession

from src.parser.codeforces.parser import Parser


@pytest.fixture
def parser():
    return Parser()


@pytest.mark.asyncio
@patch('src.parser.utils.utils.get_fresh_cookies_and_headers')
@patch('aiohttp.ClientSession')
@patch('selenium.webdriver.Chrome')
async def test_request_codeforces_successful(mock_chrome, mock_client_session, mock_get_fresh_cookies_and_headers,
                                             parser):
    mock_get_fresh_cookies_and_headers.return_value = ({}, {})
    response_mock = AsyncMock()
    response_mock.status = 200
    response_mock.json.return_value = {
        'status': 'OK',
        'result': {
            'problems': [
                {'contestId': 1, 'index': 'A', 'name': 'Test Problem', 'rating': 1500, 'tags': ['dp']}
            ],
            'problemStatistics': [
                {'contestId': 1, 'index': 'A', 'solvedCount': 123}
            ]
        }
    }

    session_mock = AsyncMock(spec=ClientSession)
    session_mock.get.return_value.__aenter__.return_value = response_mock
    mock_client_session.return_value.__aenter__.return_value = session_mock

    driver_mock = MagicMock()
    mock_chrome.return_value = driver_mock

    driver_mock.execute_script.return_value = {
        'returnValue': '{}'
    }

    results = await parser.request_codeforces()
    assert results['problems'][0]['name'] == 'Test Problem'

    mock_chrome.assert_called_once()
    driver_mock.quit.assert_called_once()


@pytest.mark.asyncio
@patch('src.db.models.task.Subject.all', new_callable=AsyncMock)
async def test_get_tags_map(mock_subject_all, parser):
    mock_subject_all.return_value = [MagicMock(tag="dp")]

    tags_map = await parser.get_tags_map()
    assert tags_map["dp"].tag == "dp"


@pytest.mark.asyncio
@patch('src.db.models.task.Contest.get_or_create', new_callable=AsyncMock)
@patch('src.db.models.task.Task.get_or_create', new_callable=AsyncMock)
async def test_process_tasks(mock_task_get_or_create, mock_contest_get_or_create, parser):
    problems = [
        {'contestId': 1, 'index': 'A', 'name': 'Test Problem', 'rating': 1500, 'tags': ['dp']}
    ]
    tags_map = {"dp": MagicMock(tag="dp")}
    problem_statistics = {"1A": 123}

    task_mock = MagicMock()
    task_mock.subject.clear = AsyncMock()
    task_mock.subject.add = AsyncMock()

    mock_task_get_or_create.return_value = (task_mock, True)
    mock_contest_get_or_create.return_value = (MagicMock(), True)

    await parser.process_tasks(problems, tags_map, problem_statistics)

    mock_task_get_or_create.assert_called_once_with(
        number='1A',
        defaults={
            'name': 'Test Problem',
            'rating': 1500,
            'url': 'https://codeforces.com/problemset/problem/1/A',
            'solved_count': 123,
        }
    )
    task_mock.subject.clear.assert_called_once()
    task_mock.subject.add.assert_called_once_with(tags_map["dp"])
