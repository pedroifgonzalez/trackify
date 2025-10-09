import pytest
from src.wakatime.client import WakaClient
import os
from src.utils.time import get_time_short_description

WAKATIME_CLIENT_ID = os.getenv("WAKATIME_CLIENT_ID")
WAKATIME_CLIENT_SECRET = os.getenv("WAKATIME_CLIENT_SECRET")
WAKATIME_REDIRECT_URI = os.getenv("WAKATIME_REDIRECT_URI")
BRANCH_NAME = os.getenv("BRANCH_NAME")


@pytest.mark.vcr
def test_get_total_time():
    waka_client = WakaClient(
        api_key=os.getenv("WAKATIME_API_KEY"),
    )
    waka_total_duration = waka_client.get_total_time(
        branch_name=BRANCH_NAME
    )
    assert waka_total_duration
    assert waka_total_duration.start
    assert waka_total_duration.end
    assert waka_total_duration.duration

    assert get_time_short_description(waka_total_duration.duration) == "2h 59m 19s"
