import datetime as dt
from datetime import date, datetime, timedelta
from typing import Any, Union

from dateutil.rrule import WEEKLY, rrule

from arrow.constants import MAX_TIMESTAMP, MAX_TIMESTAMP_MS, MAX_TIMESTAMP_US


def next_weekday(start_date, weekday):
    """Get next weekday from the specified start date.

    :param start_date: Datetime object representing the start date.
    :param weekday: Next weekday to obtain. Can be a value between 0 (Monday) and 6 (Sunday).
    :return: Datetime object corresponding to the next weekday after start_date.

    Usage::

        # Get first Monday after epoch
        >>> next_weekday(datetime(1970, 1, 1), 0)
        1970-01-05 00:00:00

        # Get first Thursday after epoch
        >>> next_weekday(datetime(1970, 1, 1), 3)
        1970-01-01 00:00:00

        # Get first Sunday after epoch
        >>> next_weekday(datetime(1970, 1, 1), 6)
        1970-01-04 00:00:00
    """
    if weekday < 0 or weekday > 6:
        raise ValueError("Weekday must be between 0 (Monday) and 6 (Sunday).")
    return rrule(freq=WEEKLY, dtstart=start_date, byweekday=weekday, count=1)[0]


def total_seconds(td: timedelta) -> float:
    """Get total seconds for timedelta."""
    return td.total_seconds()


def is_timestamp(value: Any) -> bool:
    """Check if value is a valid timestamp."""
    if isinstance(value, bool):
        return False
    if not (
        isinstance(value, int) or isinstance(value, float) or isinstance(value, str)
    ):
        return False
    try:
        float(value)
        return True
    except ValueError:
        return False


def normalize_timestamp(timestamp):
    """Normalize millisecond and microsecond timestamps into normal timestamps."""
    if timestamp > MAX_TIMESTAMP:
        if timestamp < MAX_TIMESTAMP_MS:
            timestamp /= 1e3
        elif timestamp < MAX_TIMESTAMP_US:
            timestamp /= 1e6
        else:
            raise ValueError(f"The specified timestamp '{timestamp}' is too large.")
    return timestamp


# Credit to https://stackoverflow.com/a/1700069
def iso_to_gregorian(
    iso_year: int, iso_week: int, iso_day: int
) -> Union[date, datetime]:
    """Converts an ISO week date tuple into a datetime object."""

    if not 1 <= iso_week <= 53:
        raise ValueError("ISO Calendar week value must be between 1-53.")

    if not 1 <= iso_day <= 7:
        raise ValueError("ISO Calendar day value must be between 1-7")

    # The first week of the year always contains 4 Jan.
    fourth_jan: date = dt.date(iso_year, 1, 4)
    delta: timedelta = dt.timedelta(fourth_jan.isoweekday() - 1)
    year_start: date = fourth_jan - delta
    gregorian = year_start + dt.timedelta(days=iso_day - 1, weeks=iso_week - 1)

    return gregorian


def validate_bounds(bounds):
    if bounds != "()" and bounds != "(]" and bounds != "[)" and bounds != "[]":
        raise ValueError(
            'Invalid bounds. Please select between "()", "(]", "[)", or "[]".'
        )


__all__ = ["total_seconds", "is_timestamp", "iso_to_gregorian"]
