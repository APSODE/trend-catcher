from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.model.news_topic_map_model import NewsTopicMapModel
from sqlalchemy import select

class NewsTopicMapRepository:
    #새 매핑 추가
    async def save(self, session: AsyncSession, news_id: int, topic_id: int, similarity_score: float) -> None:
        mapping = NewsTopicMapModel(
            news_id = news_id,
            topic_id = topic_id,
            similarity_score = similarity_score
        )
        session.add(mapping)
        await session.flush()

    #기사가 가진 주제들 조회
    async def get_topics_by_news(self, session: AsyncSession, news_id: int) -> list[int]:
        query = select(NewsTopicMapModel.topic_id).where(NewsTopicMapModel.news_id == news_id)
        result = await session.execute(query)
        return list(result.scalars().all())

    #주제가 가진 기사들 조회
    async def get_news_by_topic(self, session: AsyncSession, topic_id: int) -> list[int]:
        query = select(NewsTopicMapModel.news_id).where(NewsTopicMapModel.topic_id == topic_id)
        result = await session.execute(query)
        return list(result.scalars().all())