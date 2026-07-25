from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.model.news_keyword_map_model import NewsKeywordMapModel
from src.llm_api.model.keyword_model import KeywordModel
from sqlalchemy import select

class NewsKeywordMapRepository:
    #새 매핑 추가
    async def save(self, session: AsyncSession, news_id: int, keyword_id: int) -> None:
        mapping = NewsKeywordMapModel(
            news_id = news_id,
            keyword_id = keyword_id
        )
        session.add(mapping)
        await session.flush()

    #뉴스로 키워드 탐색
    async def get_keywords_by_news(self, session:AsyncSession, news_id: int) -> list[KeywordModel]:
        query = select(KeywordModel).join(NewsKeywordMapModel, NewsKeywordMapModel.keyword_id == KeywordModel.id).where(NewsKeywordMapModel.news_id == news_id)
        result = await session.execute(query)
        return list(result.scalars().all())

    #키워드로 뉴스 탐색
    async def get_news_by_keyword(self, session:AsyncSession, keyword_id: int) -> list[int]:
        query = select(NewsKeywordMapModel.news_id).where(NewsKeywordMapModel.keyword_id == keyword_id)
        result = await session.execute(query)
        return list(result.scalars().all())