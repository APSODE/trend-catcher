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
    async def fill_scores(self, limit: int) -> None:
        targets = await self._news_analysis_repository.find_unscored(limit)

        for target in targets:
            #재료 꺼내기
            topic = await self._topic_repository.get_by_pk(target.topic_fk)
            topic_count = topic.count
            content_score = target.score_detail["content_score"]

            #결과
            result = self._calculate_final_score(content_score, topic_count)

            #갱신
            await self._news_analysis_repository.update_score(target, result["score"], result["score_detail"])
        logger.info("점수 산정 완료: %d건", len(targets))


    # 중복점수 계산
    @staticmethod
    def _calculate_cross_check_score(topic_count: int) -> float:
        return min(topic_count / ScoringConstant.CROSS_CHECK_MAX, 1.0)

    #최종점수 계산
    @staticmethod
    def _calculate_final_score(content_score: float, topic_count: int) -> dict:
        cross_check_score = ScoringService._calculate_cross_check_score(topic_count)
        final_score = ScoringConstant.CONTENT_WEIGHT * content_score + ScoringConstant.CROSS_CHECK_WEIGHT * cross_check_score
        return {
            "score" : final_score,
            "score_detail" : {
                "content_score" : content_score,
                "cross_check_score" : cross_check_score,
            }
        }