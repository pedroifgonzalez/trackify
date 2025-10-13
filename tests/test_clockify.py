import datetime
from unittest.mock import MagicMock, patch

import pytest

from src.cli.commands.config import config as cfg
from src.clients.time_managers.clockify.client import ClockifyClient
from src.core.exceptions import ClientError


@pytest.mark.vcr
def test_create_time_entry():
    clockify_client = ClockifyClient(
        api_key=cfg.CLOCKIFY_API_KEY,
        workspace_id=cfg.CLOCKIFY_WORKSPACE_ID,
        project_id=cfg.CLOCKIFY_PROJECT_ID,
    )
    clockify_total_duration = clockify_client.create_time_entry(
        description="Test time entry",
        start=datetime.datetime.now() - datetime.timedelta(minutes=5),
        end=datetime.datetime.now(),
    )
    assert clockify_total_duration


def test_create_time_entry_no_success():
    clockify_client = ClockifyClient(
        api_key=cfg.CLOCKIFY_API_KEY,
        workspace_id=cfg.CLOCKIFY_WORKSPACE_ID,
        project_id=cfg.CLOCKIFY_PROJECT_ID,
    )
    with (
        patch(
            "src.clients.time_managers.clockify.client.requests.post"
        ) as mock_response,
        pytest.raises(ClientError),
    ):
        mock_response.return_value = MagicMock(status_code=400)
        clockify_client.create_time_entry(
            description="Test time entry",
            start=datetime.datetime.now() - datetime.timedelta(minutes=5),
            end=datetime.datetime.now(),
        )
