from src.llm_api.repository.search_cache_repository import SearchCacheRepository
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SearchCacheService:
    def __init__(self, repository: SearchCacheRepository):
        self._repository = repository

    async def save(self, result: dict[str, list[str]]) -> None:
        await self._repository.create_cache(result)

    async def get_latest(self, since: datetime) -> dict[str, list[str]]:
        cache = await self._repository.find_latest()
        if cache is None:
            logger.info("저장된 결과 없음")
            return {}
        if cache.searched_at < since:
            logger.info("너무 이전 결과: %s", cache.searched_at)
            return {}
        return cache.result