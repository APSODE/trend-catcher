from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.repository.topic_repository import TopicRepository

class ScoringService:
    CONTENT_WEIGHT = 0.35
    CROSS_CHECK_WEIGHT = 0.65
    CROSS_CHECK_MAX = 6  # TODO: 돌려보며 조정필요

    def __init__(self, news_analysis_repo: NewsAnalysisRepository, topic_repo: TopicRepository):
        self.news_analysis_repo = news_analysis_repo
        self.topic_repo = topic_repo

    #중복점수 계산
    def calculate_cross_check_score(self, topic_count: int) -> float:
        return min(topic_count / self.CROSS_CHECK_MAX, 1.0)

    #최종점수 계산
    def calculate_final_score(self, content_score: float, topic_count: int) -> dict:
        cross_check_score = self.calculate_cross_check_score(topic_count)
        final_score = self.CONTENT_WEIGHT * content_score + self.CROSS_CHECK_WEIGHT * cross_check_score
        return {
            "score" : final_score,
            "score_detail" : {
                "content_score" : content_score,
                "cross_check_score" : cross_check_score,
                "weights" : {
                    "content" : self.CONTENT_WEIGHT,
                    "cross_check" : self.CROSS_CHECK_WEIGHT
                }
            }
        }

    #db에서 점수 없는 뉴스들 채워주기
    async def fill_scores(self, session:AsyncSession) -> None:
        targets = await self.news_analysis_repo.get_unscored_news(session)

        for news in targets:
            topic = await self.topic_repo.get(session, news.topic_id)
            content_score = news.score_detail["content_score"]

            result = self.calculate_final_score(content_score, topic.count)
            news.score = result["score"]
            news.score_detail = result["score_detail"]

        await session.commit()
