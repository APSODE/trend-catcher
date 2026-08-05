from datetime import datetime


def normalize_datetime(dt: datetime) -> datetime:
    dt = dt.replace(tzinfo = None, microsecond = 0)
    return dt

def now_normalized() -> datetime:
    return normalize_datetime(datetime.now())