from src.llm_api.repository.base_repository import BaseRepository
from src.llm_api.model.keyword_model import KeywordModel
from sqlalchemy.ext.asyncio import AsyncSession

class KeywordRepository(BaseRepository[KeywordModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, KeywordModel)

    #키워드들로 찾기
    async def find_by_keywords(self, keywords: list[str]) -> list[KeywordModel]:
        if not keywords: #빈 리스트 방어
            return []
        return await self._find_all(KeywordModel.keyword.in_(keywords))

    #모델 포장
    async def create_keyword(self, keyword: str, embedding: list[float]) -> KeywordModel:
        new_keyword = KeywordModel(keyword = keyword, embedding = embedding)
        return await self.save(new_keyword)