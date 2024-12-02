import datetime
import pytz
from datetime import datetime as Date


def format_datetime(dt: Date) -> str:
    """
    Format a datetime object as an ISO string.

    Args:
        dt (Date): The datetime object to format.

    Returns:
        str: The formatted datetime as an ISO string.
    """

    return datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S")


def minutes_today_as_iso(date: Date, minutes: int, timezone: str) -> str:
    """
    Return the current date with the given minutes as an ISO string.

    Args:
        date (Date): The current date.
        minutes (int): The minutes to add to the current date.
        timezone (str): The timezone to use.

    Returns:
        str: The formatted datetime as an ISO string.
    """

    return (
        format_datetime(
            date.replace(hour=0, minute=0, second=0, microsecond=0)
            + datetime.timedelta(minutes=minutes)
        )
        + timezone
    )


def minutes_as_datetime(
    date: datetime.datetime, minutes: int, timezone: str
) -> datetime.datetime:
    """
    Add minutes to a datetime object and return the new datetime object with the timezone applied.

    Args:
        date (datetime.datetime): The datetime object to add minutes to.
        minutes (int): The minutes to add.
        timezone (str): The timezone to apply.

    Returns:
        datetime.datetime: The new datetime object with the timezone applied.
    """

    new_time = date.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + datetime.timedelta(minutes=minutes)

    # Zeitzone anwenden
    tz = pytz.timezone(timezone)
    return tz.localize(new_time)
