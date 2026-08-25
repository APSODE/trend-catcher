from src.llm_api.constant.period_constant import PeriodConstant
from src.llm_api.dependency import MajorNewsServiceDep
from src.llm_api.schema.response import NewsResponseData
from src.llm_api.util.datetime_util import DateTimeUtil
from fastapi import APIRouter

router = APIRouter(prefix="/news", tags=["News"])

@router.get("/daily", response_model = list[NewsResponseData])
async def get_daily_news(service: MajorNewsServiceDep, limit: int) -> list[NewsResponseData]:
    since = DateTimeUtil.get_current_period_start(PeriodConstant.MORNING_HOUR, PeriodConstant.EVENING_HOUR)
    until = DateTimeUtil.get_previous_period_start(PeriodConstant.MORNING_HOUR, PeriodConstant.EVENING_HOUR)
    return await service.get_major_news(since, until, limit)