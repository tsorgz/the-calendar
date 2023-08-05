from datetime import datetime, timezone
from pytz import timezone as get_timezone


class ISOTimestampParseError(Exception):
    """A custom Exception assoicated with parsing ISO 8601 timestamps"""

    def __init__(self):
        super().__init__(
            "Timestamp is not parseable, please refer to https://www.iso.org/iso-8601-date-and-time-format.html for formatting."
        )


def parse_timestamp_info(timestamp: str):
    """Parses a timestamp from its string representation into a proper datetime.

    Args:
        timestamp (str): The timestamp to be parsed.

    Returns:
        A 2-length tuple containing the datetime and a bool with parsed timestamp information.
            [0] (datetime.datetime): The parsed timestamp.
            [1] (bool): Whether or not the timestamp has a timezone associated.

    Raises:
        ISOTimestampParseError: A timestamp could not be parsed due to violating ISO 8601 or being a valid ordinal timestamp.
    """
    dt = None

    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        raise ISOTimestampParseError()

    if dt.tzinfo and dt.tzinfo != timezone.utc:
        dt = dt.astimezone(timezone.utc)

    return dt, dt.tzinfo != None


def apply_tz_to_datetime(dt: datetime, tz: str):
    tz_obj = get_timezone(tz)
    dt = tz_obj.localize(dt)
    if dt.tzinfo != timezone.utc:
        dt = dt.astimezone(timezone.utc)
    return dt
