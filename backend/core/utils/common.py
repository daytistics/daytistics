import datetime

def ensure_timezone_aware(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt