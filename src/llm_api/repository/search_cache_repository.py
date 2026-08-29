from src.llm_api.repository.base_repository import BaseRepository
from src.llm_api.model.search_cache_model import SearchCacheModel
from sqlalchemy.ext.asyncio import AsyncSession

class SearchCacheRepository(BaseRepository[SearchCacheModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, SearchCacheModel)

    #최근 스냅샷(아몰라여기만들어)
    async def find_latest(self) -> SearchCacheModel | None:
        stmt = self._select().order_by(SearchCacheModel.searched_at.desc()).limit(1)
        return await self._session.scalar(stmt)

    #모델 포장
    async def create_cache(self, result: dict[str, list[str]]) -> SearchCacheModel:
        new_cache = SearchCacheModel(result = result)
        return await self.save(new_cache)