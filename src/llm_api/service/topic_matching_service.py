from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

from src.llm_api.model.topic_model import TopicModel
from src.llm_api.repository.news_topic_map_repository import NewsTopicMapRepository
from src.llm_api.service.embedding_service import EmbeddingService
from src.llm_api.repository.topic_repository import TopicRepository

@dataclass
class TopicMatchData:
    candidates_topics: list
    main_topic_id: int
    main_topic_count: int
    is_new_topic: bool

class TopicMatchingService:
    SELF_SIMILARITY = 1.0 #

    def __init__(self, topic_repo: TopicRepository, news_topic_map_repo: NewsTopicMapRepository, embedding_service: EmbeddingService):
        self.topic_repo = topic_repo
        self.news_topic_map_repo = news_topic_map_repo
        self.embedding_service = embedding_service

    #임베딩값 받아서 매칭시키고 결과반환
    async def create_topic_match_data(self, session: AsyncSession, embedding: list[float], news_id: str, topic_name: str) -> TopicMatchData:
        topic_list = await self.topic_repo.get_all(session)

        candidates = []
        for topic in topic_list:
            similarity_score = self.embedding_service.get_similarity_score(embedding, topic.representative_embedding)
            if self.embedding_service.classify_similarity(similarity_score) != "no_match":
                candidates.append([topic, similarity_score])

        candidates.sort(key = lambda pair: pair[1], reverse = True)

        if not candidates: #후보가 없으면 새 후보 만들고 함수 탈출
            new_topic_model = TopicModel(
                topic_name = topic_name,
                representative_news_id = news_id,
                representative_embedding = embedding
            )
            new_topic = await self.topic_repo.save(session, new_topic_model)
            return TopicMatchData(
                candidates_topics= [],
                main_topic_id = new_topic.id,
                main_topic_count = new_topic.count,
                is_new_topic= True
            )

        main_topic = candidates[0][0]
        await self.topic_repo.increment_count(session, main_topic.id)
        return TopicMatchData(
            candidates_topics= candidates,
            main_topic_id = main_topic.id,
            main_topic_count = main_topic.count,
            is_new_topic = False
        )

    #결과 반영
    async def save_topic_match_data(self, session: AsyncSession, news_id: int, match_data: TopicMatchData) -> None:
        if match_data.is_new_topic:
            await self.news_topic_map_repo.save(session, news_id, match_data.main_topic_id, self.SELF_SIMILARITY)
            return
        for topic, similarity_score in match_data.candidates_topics:
            await self.news_topic_map_repo.save(session, news_id, topic.id, similarity_score)