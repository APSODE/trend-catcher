from datetime import datetime
from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.schema.response import NewsResponseData

class MajorNewsService:
    def __init__(self, news_analysis_repository: NewsAnalysisRepository):
        self._news_analysis_repository = news_analysis_repository

    async def get_major_news(self, since: datetime) -> list[NewsResponseData]:
        news_list = await self._news_analysis_repository.find_scored_since(since) #여기서 score가 None이 아닌 거만 받으므로 아래 타입경고 무시
        selected = self._pick_top_by_topic(news_list)
        return [NewsResponseData(crawled_id = news.crawled_id, score = news.score) for news in sorted(selected, key = lambda news: news.score, reverse = True)]

    @staticmethod
    def _pick_top_by_topic(news_list: list[NewsAnalysisModel]) -> list[NewsAnalysisModel]:
        best_by_topic: dict[int, NewsAnalysisModel] = {}
        for news in news_list:
            current = best_by_topic.get(news.topic_fk)
            if current is None or news.score > current.score:
                best_by_topic[news.topic_fk] = news
        return list(best_by_topic.values())
