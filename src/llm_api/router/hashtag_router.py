from src.llm_api.dependency import HashtagPreparerDep, HashtagSearchServiceDep, SearchCacheServiceDep
from src.llm_api.schema.request import HashtagSearchRequestData
from src.llm_api.schema.response import HashtagPrepareResponseData
from fastapi import APIRouter
from src.llm_api.util.datetime_util import DateTimeUtil
from src.llm_api.constant.period_constant import PeriodConstant

router = APIRouter(prefix="/hashtag", tags=["Hashtag"])

@router.post("/prepare", response_model = HashtagPrepareResponseData)
async def prepare_hashtags(preparer: HashtagPreparerDep) -> HashtagPrepareResponseData:
    result = await preparer.run()
    return HashtagPrepareResponseData(total = result.total, prepared = result.prepared, failed = result.failed)

@router.post("/search", response_model = dict[str, list[str]])
async def search_hashtags(request: HashtagSearchRequestData, service: HashtagSearchServiceDep, cache_service: SearchCacheServiceDep) -> dict[str, list[str]]:
    since = DateTimeUtil.get_previous_period_start(PeriodConstant.MORNING_HOUR, PeriodConstant.EVENING_HOUR)
    until = DateTimeUtil.get_current_period_start(PeriodConstant.MORNING_HOUR, PeriodConstant.EVENING_HOUR)
    result = await service.search_all(request.hashtags, since, until)
    await cache_service.save(result)
    return result

@router.get("/latest", response_model = dict[str, list[str]])
async def get_latest_search(cache_service: SearchCacheServiceDep) -> dict[str, list[str]]:
    since = DateTimeUtil.get_previous_period_start(PeriodConstant.MORNING_HOUR, PeriodConstant.EVENING_HOUR)
    return await cache_service.get_latest(since)