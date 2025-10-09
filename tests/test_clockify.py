import datetime
import os

import pytest

from src.clockify.client import ClockifyClient

CLOCKIFY_API_KEY = os.getenv("CLOCKIFY_API_KEY")
WORKSPACE_ID = os.getenv("WORKSPACE_ID")
PROJECT_ID = os.getenv("PROJECT_ID")


@pytest.mark.vcr
def test_create_time_entry():
    clockify_client = ClockifyClient(
        api_key=CLOCKIFY_API_KEY, workspace_id=WORKSPACE_ID, project_id=PROJECT_ID
    )
    clockify_total_duration = clockify_client.create_time_entry(
        description="Test time entry",
        start=datetime.datetime.now() - datetime.timedelta(minutes=5),
        end=datetime.datetime.now(),
    )
    assert clockify_total_duration
