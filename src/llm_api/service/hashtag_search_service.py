from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.model.hashtag_model import HashtagModel
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from src.llm_api.schema.keyword_query import KeywordQueryData
from src.llm_api.service.hashtag_expansion_service import HashtagExpansionService
from src.llm_api.service.keyword_matching_service import KeywordMatchingService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HashtagSearchService:
    def __init__(self, expansion_service: HashtagExpansionService, keyword_matching_service: KeywordMatchingService, news_keyword_map_repository: NewsKeywordMapRepository, news_analysis_repository: NewsAnalysisRepository):
        self._expansion_service = expansion_service
        self._keyword_matching_service = keyword_matching_service
        self._news_keyword_map_repository = news_keyword_map_repository
        self._news_analysis_repository = news_analysis_repository

    #해시태그별 뉴스 pk 반환
    async def search_all(self, hashtags: list[str], since: datetime, until: datetime) -> dict[str, list[str]]:
        #빈 리스트 방어
        if not hashtags:
            return {}

        #전체 확장
        expanded_list = await self._expansion_service.get_or_expand_all(hashtags)

        #포장 후 키워드 매칭
        queries = [self._to_query(expanded) for expanded in expanded_list]
        keyword_pk_list = await self._keyword_matching_service.find_matching_pks(queries)

        #매칭된 키워드로 뉴스 연결
        return await self._collect_crawled_ids(expanded_list, keyword_pk_list)

    #확장 데이터를 검색어로 포장
    def _to_query(self, expanded: HashtagModel) -> KeywordQueryData:
        return KeywordQueryData(terms = [expanded.hashtag, *expanded.aliases, *expanded.children], embedding = expanded.embedding)

    #해시태그별 매칭된 키워드로 뉴스 매칭
    async def _collect_crawled_ids(self, expanded_list: list[HashtagModel], keyword_pk_list: list[set[int]], since: datetime, until: datetime, limit: int = 10) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for expanded, keyword_pks in zip(expanded_list, keyword_pk_list):
            news_pks = await self._news_keyword_map_repository.find_news_fks_by_keyword_fks(list(keyword_pks))
            news_list = await self._news_analysis_repository.find_scored_between_by_pks(news_pks, since, until)
            selected = self._pick_top_by_topic(news_list)
            top = sorted(selected, key = lambda news: news.score, reverse = True)[:limit]
            result[expanded.hashtag] = [news.crawled_id for news in top]
            logger.debug("해시태그 검색: [%s, 후보 %d건 중 %d건]", expanded.hashtag, len(news_list), len(top))
        return result

    #주제별 최고 한건만
    @staticmethod
    def _pick_top_by_topic(news_list: list[NewsAnalysisModel]) -> list[NewsAnalysisModel]:
        best_by_topic: dict[int, NewsAnalysisModel] = {}
        for news in news_list:
            current = best_by_topic.get(news.topic_fk)
            if current is None or news.score > current.score:
                best_by_topic[news.topic_fk] = news
            return list(best_by_topic.values())
