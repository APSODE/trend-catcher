from datetime import datetime, date
from zoneinfo import ZoneInfo

KST = ZoneInfo("Asia/Seoul")

def normalize_datetime(dt: datetime) -> datetime:
    return dt.replace(microsecond=0)

def now_normalized() -> datetime:
    return datetime.now(KST).replace(microsecond=0)

def now_date() -> date:
    return now_normalized().date()