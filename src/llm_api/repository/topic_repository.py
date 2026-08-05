from src.llm_api.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.model.topic_model import TopicModel
from datetime import datetime
from sqlalchemy import update

class TopicRepository(BaseRepository[TopicModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, TopicModel)

    #12시간 범위 검색
    async def find_recent(self, since: datetime) -> list[TopicModel]:
        return await self._find_all(TopicModel.first_found_at >= since)

    #주제 중복도 증가
    async def increment_count(self, pk: int) -> None:
        await self._update(TopicModel.pk == pk, {"count" : TopicModel.count + 1})

    #모델 포장
    async def create_topic(self, topic: str, representative_crawled_id: str, representative_embedding: list[float]) -> TopicModel:
        new_topic = TopicModel(
            topic = topic,
            representative_crawled_id = representative_crawled_id,
            representative_embedding = representative_embedding
        )
        return await self.save(new_topic)