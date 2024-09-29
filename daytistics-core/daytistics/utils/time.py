import datetime
import pytz
from datetime import datetime as Date


def format_datetime(dt: Date):
    return datetime.datetime.strftime(dt, "%Y-%m-%dT%H:%M:%S")


def minutes_today_as_iso(date: Date, minutes: int, timezone: str) -> str:
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
    new_time = date.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + datetime.timedelta(minutes=minutes)

    # Zeitzone anwenden
    tz = pytz.timezone(timezone)
    return tz.localize(new_time)
