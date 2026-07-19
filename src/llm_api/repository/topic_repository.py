from sqlalchemy.ext.asyncio import AsyncSession
from model.topic_model import TopicModel
from sqlalchemy import select

class TopicRepository:
    #새 주제 추가
    async def save(self, session: AsyncSession, topic: TopicModel) -> TopicModel:
        session.add(topic)
        await session.flush()
        return topic

    #주제 목록 반환
    async def get_all(self, session: AsyncSession) -> list[TopicModel]:
        query = select(TopicModel)
        result = await session.execute(query)
        return list(result.scalars().all())

    #주제 중복도 증가
    async def increment_count(self, session: AsyncSession, topic_id: int) -> None:
        topic = await session.get(TopicModel, topic_id)
        topic.count += 1
        await session.flush()