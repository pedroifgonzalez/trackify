from datetime import datetime
from zoneinfo import ZoneInfo


def get_time_short_description(duration: float) -> str:
    """Get time duration expressed in short description

    Args:
        duration (float): Duration in seconds

    Returns:
        str: Duration expressed in short description
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
    """
    dt = datetime.fromtimestamp(timestamp, tz=ZoneInfo("UTC"))
    return dt.astimezone(ZoneInfo(timezone))


def beautify_datetime(dt: datetime) -> str:
    """Format a datetime object to a human-readable string.

    Args:
        dt (datetime): The datetime object to format.

    Returns:
        str: The beautified datetime string.
    """
    return dt.strftime("%Y-%m-%d %I:%M:%S %p")
