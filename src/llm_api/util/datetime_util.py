from datetime import datetime, timedelta, timezone

class DateTimeUtil:
    KST = timezone(timedelta(hours = 9))

    @staticmethod
    def now_kst() -> datetime:
        return datetime.now(DateTimeUtil.KST).replace(tzinfo = None)