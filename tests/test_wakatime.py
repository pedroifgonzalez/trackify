import datetime

import pytest

from src.cli.commands.config import config as cfg
from src.clients.activity_trackers.wakatime.client import WakaClient
from src.utils.time import get_time_short_description


@pytest.mark.vcr
def test_get_total_time():
    waka_client = WakaClient(
        api_key=cfg.WAKATIME_API_KEY,
    )
    waka_total_duration = waka_client.get_total_time(
        branch_name="fix/improve-approval-notification-email-content",
        project_name="media_service_poc",
        search_date=datetime.date(2025, 10, 8),
    )
    assert waka_total_duration
    assert waka_total_duration.start
    assert waka_total_duration.end
    assert waka_total_duration.duration

    assert get_time_short_description(waka_total_duration.duration) == "0h 4m 37s"
