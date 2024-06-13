import pytest
from unittest.mock import AsyncMock, create_autospec, patch

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.parser.codeforces.parser import Parser
from src.parser.parser_manager import ParserManager
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED


@pytest.fixture
def parser_manager():
    parser_mock = create_autospec(Parser)
    return ParserManager(parser_mock)


@pytest.mark.asyncio
async def test_job_listener(parser_manager):
    with patch('logging.info') as mock_logging_info, \
            patch('logging.error') as mock_logging_error, \
            patch('logging.warning') as mock_logging_warning:
        event_executed = AsyncMock(code=EVENT_JOB_EXECUTED, job_id='test_job', scheduled_run_time='now')
        event_error = AsyncMock(code=EVENT_JOB_ERROR, job_id='test_job', exception=Exception('Test error'),
                                traceback='traceback')
        event_missed = AsyncMock(code=EVENT_JOB_MISSED, job_id='test_job', scheduled_run_time='now')

        parser_manager.job_listener(event_executed, event_error)
        parser_manager.job_listener(event_error, event_missed)
        parser_manager.job_listener(event_missed, event_executed)

        mock_logging_info.assert_any_call('Job test_job executed successfully at now')
        mock_logging_error.assert_any_call('Job test_job failed with exception: Test error')
        mock_logging_error.assert_any_call('Traceback: traceback')
        mock_logging_warning.assert_any_call('Job test_job missed at now')


@pytest.mark.asyncio
async def test_start_scheduler(parser_manager):
    with patch.object(AsyncIOScheduler, 'start', new_callable=AsyncMock) as mock_start, \
            patch.object(AsyncIOScheduler, 'add_job') as mock_add_job, \
            patch.object(AsyncIOScheduler, 'add_listener') as mock_add_listener:
        await parser_manager.start_scheduler()

        assert parser_manager.scheduler is not None
        mock_add_job.assert_called_once_with(parser_manager.parser.parse, 'interval', seconds=3600)
        mock_add_listener.assert_called_once()
        mock_start.assert_awaited_once()


@pytest.mark.asyncio
async def test_shutdown(parser_manager):
    scheduler_mock = AsyncMock()
    parser_manager.scheduler = scheduler_mock
    await parser_manager.shutdown()
    scheduler_mock.shutdown.assert_called_once_with(wait=False)
