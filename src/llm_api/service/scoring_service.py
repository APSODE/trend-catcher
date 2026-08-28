from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from src.llm_api.constant.scoring_constant import ScoringConstant
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.repository.topic_repository import TopicRepository
import logging

logger = logging.getLogger(__name__)

class ScoringService:
    def __init__(self, news_analysis_repository: NewsAnalysisRepository, topic_repository: TopicRepository):
        self._news_analysis_repository = news_analysis_repository
        self._topic_repository = topic_repository

    #score가 None인것들 채우기
    async def fill_scores(self) -> int:
        targets = await self._news_analysis_repository.find_unscored()
        for target in targets:
            await self._fill_one(target)
        logger.info("점수 산정 완료: %d건", len(targets))
        return len(targets)

    async def _fill_one(self, target: NewsAnalysisModel):
        topic = await self._topic_repository.get_by_pk(target.topic_fk)
        cross_check_score = self._calculate_cross_check_score(topic.count)
        score = self._calculate_final_score(target.content_score, cross_check_score)
        await self._news_analysis_repository.update_score(target, score, cross_check_score)

    #중복점수 계산
    @staticmethod
    def _calculate_cross_check_score(topic_count: int) -> float:
        return min(topic_count / ScoringConstant.CROSS_CHECK_MAX, 1.0)

    @staticmethod
    def _calculate_final_score(content_score: float, cross_check_score: float) -> float:
        return ScoringConstant.CONTENT_WEIGHT * content_score + ScoringConstant.CROSS_CHECK_WEIGHT * cross_check_score