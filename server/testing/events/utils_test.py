import pytest
from pytz import UnknownTimeZoneError
from datetime import datetime, timezone
from events.utils import (
    parse_timestamp_info,
    apply_tz_to_datetime,
    ISOTimestampParseError,
)


@pytest.mark.parametrize(
    "ts, dt, err",
    [
        ("2021-01-01", datetime(2021, 1, 1), False),
        ("2021-01-01T05", datetime(2021, 1, 1, 5), False),
        ("2021-01-01T05:30", datetime(2021, 1, 1, 5, 30), False),
        ("2021-01-01T05:30:45", datetime(2021, 1, 1, 5, 30, 45), False),
        ("2021-01-01T05:30:45.12345", None, True),
        (
            "2021-01-01+00:00",
            datetime(2021, 1, 1, tzinfo=timezone.utc),
            False,
        ),  # TODO: Flagged as bug, should invalidate in code, result makes naive dt 2021/01/01 00:00
        ("2021-01-01T05+04:00", datetime(2021, 1, 1, 1, tzinfo=timezone.utc), False),
        (
            "2021-01-01T05:30-06:30",
            datetime(2021, 1, 1, 12, 0, tzinfo=timezone.utc),
            False,
        ),
        (
            "2021-01-01T05:30:45Z",
            datetime(2021, 1, 1, 5, 30, 45, tzinfo=timezone.utc),
            False,
        ),
        ("20210101", None, True),
    ],
)
def test_parse_timestamp_info(ts, dt, err):
    if err:
        with pytest.raises(ISOTimestampParseError):
            parse_timestamp_info(ts)
    else:
        test_dt, has_tz = parse_timestamp_info(ts)
        assert test_dt == dt
        assert has_tz == (dt.tzinfo is not None)


@pytest.mark.parametrize(
    "dt, tz, exp, err",
    [
        (datetime(2021, 1, 1), "UTC", datetime(2021, 1, 1, tzinfo=timezone.utc), False),
        (
            datetime(2021, 1, 1),
            "America/New_York",
            datetime(2021, 1, 1, 5, tzinfo=timezone.utc),
            False,
        ),
        (
            datetime(2021, 1, 1),
            "Europe/London",
            datetime(2021, 1, 1, tzinfo=timezone.utc),
            False,
        ),
        (
            datetime(2021, 1, 1),
            "Asia/Hong_Kong",
            datetime(2020, 12, 31, 16, tzinfo=timezone.utc),
            False,
        ),
        (
            datetime(2021, 1, 1),
            "Invalid",
            datetime(2021, 1, 1, tzinfo=timezone.utc),
            True,
        ),
    ],
)
def test_apply_tz_to_datetime(dt, tz, exp, err):
    if err:
        with pytest.raises(UnknownTimeZoneError):
            apply_tz_to_datetime(dt, tz)
    else:
        test_dt = apply_tz_to_datetime(dt, tz)
        assert test_dt == exp
