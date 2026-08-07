from datetime import datetime, timedelta, timezone

class DateTimeUtil:
    KST = timezone(timedelta(hours = 9))

    #KST 리턴
    @staticmethod
    def get_now_kst() -> datetime:
        return datetime.now(DateTimeUtil.KST).replace(tzinfo = None)

    #지금 어느 타임인지 파악
    @staticmethod
    def get_current_period_start(morning_hour: int, evening_hour: int) -> datetime:
        now = DateTimeUtil.get_now_kst()
        if now.hour >= evening_hour: #저녁시간 이후면 저녁
            return DateTimeUtil._get_current_period(now, evening_hour)
        if now.hour >= morning_hour: #저녁시간 앞이고 아침시간 이후면 아침
            return DateTimeUtil._get_current_period(now, morning_hour)
        return DateTimeUtil._get_current_period((now - timedelta(days = 1)), evening_hour) #둘 다 아니면 날짜 지난 새벽 -> 전날 저녁

    #정각 시간 반환
    @staticmethod
    def _get_current_period(now: datetime, hour: int) -> datetime:
        return now.replace(hour = hour, minute = 0, second = 0, microsecond = 0)