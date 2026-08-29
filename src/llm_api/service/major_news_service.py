from datetime import datetime
from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.schema.response import NewsResponseData
import logging

logger = logging.getLogger(__name__)

class MajorNewsService:
    def __init__(self, news_analysis_repository: NewsAnalysisRepository):
        self._news_analysis_repository = news_analysis_repository

    async def get_major_news(self, since: datetime, until: datetime, limit: int) -> list[NewsResponseData]:
        news_list = await self._news_analysis_repository.find_scored_between(since, until) #여기서 score가 None이 아닌 거만 받으므로 아래 타입경고 무시
        selected = self._pick_top_by_topic(news_list)
        result = sorted(selected, key = lambda news: news.score, reverse = True)[:limit]
        logger.info("주요 뉴스 반환: [전체 %d건 중 %d건]", len(news_list), len(result))
        return [NewsResponseData(crawled_id = news.crawled_id, score = news.score) for news in result]

    @staticmethod
    def _pick_top_by_topic(news_list: list[NewsAnalysisModel]) -> list[NewsAnalysisModel]:
        best_by_topic: dict[int, NewsAnalysisModel] = {}
        for news in news_list:
            current = best_by_topic.get(news.topic_fk)
            if current is None or news.score > current.score:
                best_by_topic[news.topic_fk] = news
        return list(best_by_topic.values())
