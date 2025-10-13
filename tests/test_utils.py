import datetime
import zoneinfo

import pytest

from src.utils.time import (
    beautify_datetime,
    convert_timestamp_with_timezone,
    get_time_short_description,
)


@pytest.mark.parametrize(
    "duration, expected",
    [
        (3661, "1h 1m 1s"),
        (7200, "2h 0m 0s"),
        (90, "0h 1m 30s"),
        (45, "0h 0m 45s"),
        (0, "0h 0m 0s"),
        (3600 * 24 + 65, "24h 1m 5s"),
    ],
)
def test_get_time_short_description(duration, expected):
    assert get_time_short_description(duration) == expected


def test_convert_timestamp_with_timezone():
    assert convert_timestamp_with_timezone(
        1759960320.983, "America/Havana"
    ) == datetime.datetime(
        2025, 10, 8, 17, 52, 0, 983000, tzinfo=zoneinfo.ZoneInfo(key="America/Havana")
    )


def test_beautify_datetime():
    assert (
        beautify_datetime(
            datetime.datetime(
                2025,
                10,
                8,
                17,
                52,
                0,
                983000,
                tzinfo=zoneinfo.ZoneInfo(key="America/Havana"),
            )
        )
        == "2025-10-08 05:52:00 PM"
    )
