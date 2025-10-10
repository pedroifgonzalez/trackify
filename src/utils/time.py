from datetime import datetime
from zoneinfo import ZoneInfo


def get_time_short_description(duration: float) -> str:
    """Get time duration expressed in short description

    Args:
        duration (float): Duration in seconds

    Returns:
        str: Duration expressed in short description

    Examples:
        >>> get_time_short_description(3661)  # 1 hour, 1 minute, 1 second
        '1h 1m 1s'
        >>> get_time_short_description(7200)  # 2 hours exactly
        '2h 0m 0s'
        >>> get_time_short_description(90)    # 1 minute, 30 seconds
        '0h 1m 30s'
        >>> get_time_short_description(45)    # 45 seconds
        '0h 0m 45s'
        >>> get_time_short_description(0)     # Zero duration
        '0h 0m 0s'
        >>> get_time_short_description(3600 * 24 + 65)  # 1 day and 1 minute, 5 seconds
        '24h 1m 5s'
    """
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    desc = f"{hours}h {minutes}m {seconds}s"
    return desc


def convert_timestamp_with_timezone(timestamp: float, timezone: str) -> datetime:
    """Get datetime adjusted to a specific timezone.

    Args:
        timestamp (float): Timestamp to convert.
        timezone (str): Target timezone name (e.g., "America/Havana").

    Returns:
        datetime: Datetime converted to the specified timezone.

    Examples:
        >>> convert_timestamp_with_timezone(1759960320.983, "America/Havana")
        datetime.datetime(2025, 10, 8, 17, 52, 0, 983000, tzinfo=zoneinfo.ZoneInfo(key='America/Havana'))
    """
    dt = datetime.fromtimestamp(timestamp, tz=ZoneInfo("UTC"))
    return dt.astimezone(ZoneInfo(timezone))


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
