from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.model.keyword_model import KeywordModel
from sqlalchemy import select

class KeywordRepository:
    #겹치는거 있나 조회
    async def get(self, session: AsyncSession, keyword: str) -> KeywordModel | None:
        query = select(KeywordModel).where(KeywordModel.keyword == keyword)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    #새 키워드 추가
    async def create(self, session:AsyncSession, keyword: str, embedding: list[float]) -> KeywordModel:
        keyword = KeywordModel(keyword = keyword, embedding = embedding)
        session.add(keyword)
        await session.flush()
        return keyword

    #다 반환
    async def get_all(self, session: AsyncSession) -> list[KeywordModel]:
        result = await session.execute(select(KeywordModel))
        return list(result.scalars().all())