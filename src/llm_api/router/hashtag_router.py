from src.llm_api.dependency import HashtagPreparerDep, HashtagSearchServiceDep
from src.llm_api.schema.request import HashtagSearchRequestData
from src.llm_api.schema.response import HashtagPrepareResponseData
from fastapi import APIRouter

router = APIRouter(prefix="/hashtag", tags=["Hashtag"])

@router.post("/prepare", response_model = HashtagPrepareResponseData)
async def prepare_hashtags(preparer: HashtagPreparerDep) -> HashtagPrepareResponseData:
    result = await preparer.run()
    return HashtagPrepareResponseData(total = result.total, prepared = result.prepared, failed = result.failed)

@router.post("/search", response_model = dict[str, list[str]])
async def search_hashtags(request: HashtagSearchRequestData, service: HashtagSearchServiceDep) -> dict[str, list[str]]:
    return await service.search_all(request.hashtags)