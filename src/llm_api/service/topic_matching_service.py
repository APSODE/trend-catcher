from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.model.topic_model import TopicModel
from src.llm_api.repository.topic_repository import TopicRepository
from src.llm_api.util.datetime_util import DateTimeUtil
from src.llm_api.util.similarity_util import SimilarityUtil
from src.llm_api.constant.period_constant import PeriodConstant
from src.llm_api.constant.similarity_constant import SimilarityConstant
from src.llm_api.constant.nvidia_constant import EmbeddingInputType
import logging

logger = logging.getLogger(__name__)

class TopicMatchingService:
    def __init__(self, client: NvidiaClient, topic_repository: TopicRepository):
        self._client = client
        self._topic_repository = topic_repository

    async def match_or_create(self, topic:str, crawled_id: str) -> TopicModel:
        embedding = await self._client.create_embedding(topic, EmbeddingInputType.PASSAGE) #주제 임베딩
        since = DateTimeUtil.get_current_period_start(PeriodConstant.MORNING_HOUR, PeriodConstant.EVENING_HOUR)
        candidates = await self._topic_repository.find_recent(since) #이번타임 주제목록

        if not candidates:  # 후보 없으면 바로 생성
            logger.debug("신규 토픽 생성 topic=%s", topic)
            return await self._topic_repository.create_topic(topic, crawled_id, embedding)

        #가장 잘 맞는 뉴스 찾기
        best_match = SimilarityUtil.find_most_similar(embedding, [candidate.representative_embedding for candidate in candidates])
        best_match_index, best_match_similarity = best_match

        matched_topic = candidates[best_match_index]
        if best_match_similarity >= SimilarityConstant.TOPIC_THRESHOLD: #기준점수 이상이면 거기 편입
            await self._topic_repository.increment_count(matched_topic.pk)
            logger.debug("토픽 편입 성공 [pk: %d, 편입된 주제:%s, 유사도=%.3f]",matched_topic.pk, candidates[best_match_index].topic, best_match_similarity)
            return matched_topic
        else:
            logger.debug("토픽 편입 실패: [pk: %d , 최고 유사 주제: %s, 유사도: %.3f]",matched_topic.pk, candidates[best_match_index].topic, best_match_similarity,)

        #아니면 새로 만듦
        logger.debug("신규 토픽 생성 topic=%s", topic)
        return await self._topic_repository.create_topic(topic, crawled_id, embedding)