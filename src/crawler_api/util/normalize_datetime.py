from datetime import datetime, date


def normalize_datetime(dt: datetime) -> datetime:
    dt = dt.replace(tzinfo=None, microsecond=0)
    return dt

def now_normalized() -> datetime:
    return normalize_datetime(datetime.now())

def now_date() -> date:
    return now_normalized().date()