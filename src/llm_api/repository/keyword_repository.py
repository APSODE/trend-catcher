from src.llm_api.repository.base_repository import AbstractBaseRepository
from src.llm_api.model.keyword_model import KeywordModel
from sqlalchemy.ext.asyncio import AsyncSession

class KeywordRepository(AbstractBaseRepository[KeywordModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, KeywordModel)

    #키워드로 찾기
    async def find_by_keyword(self, keyword: str) -> KeywordModel | None:
        return await self._find_one(KeywordModel.keyword == keyword)

    #다 꺼내기
    async def find_all(self) -> list[KeywordModel]:
        return await self._find_all()

    #모델 포장
    async def create_keyword(self, keyword: str, embedding: list[float]) -> KeywordModel:
        new_keyword = KeywordModel(keyword = keyword, embedding = embedding)
        return await self.save(new_keyword)