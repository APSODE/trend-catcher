from src.llm_api.model.hashtag_model import HashtagModel
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from src.llm_api.schema.keyword_query import KeywordQueryData
from src.llm_api.service.hashtag_expansion_service import HashtagExpansionService
from src.llm_api.service.keyword_matching_service import KeywordMatchingService
import logging

logger = logging.getLogger(__name__)

class HashtagSearchService:
    def __init__(self, expansion_service: HashtagExpansionService, keyword_matching_service: KeywordMatchingService, news_keyword_map_repository: NewsKeywordMapRepository):
        self._expansion_service = expansion_service
        self._keyword_matching_service = keyword_matching_service
        self._news_keyword_map_repository = news_keyword_map_repository

    #해시태그별 뉴스 pk 반환
    async def search_all(self, hashtags: list[str]) -> dict[str, list[int]]:
        #빈 리스트 방어
        if not hashtags:
            return {}

        #전체 확장
        expanded_list = await self._expansion_service.get_or_expand_all(hashtags)

        #포장 후 키워드 매칭
        queries = [self._to_query(expanded) for expanded in expanded_list]
        keyword_pk_list = await self._keyword_matching_service.find_matching_pks(queries)

        #매칭된 키워드로 뉴스 연결
        return await self._collect_news_pks(expanded_list, keyword_pk_list)

    #확장 데이터를 검색어로 포장
    def _to_query(self, expanded: HashtagModel) -> KeywordQueryData:
        return KeywordQueryData(terms = [expanded.hashtag, *expanded.aliases, *expanded.children], embedding = expanded.embedding)

    #해시태그별 매칭된 키워드로 뉴스 매칭
    async def _collect_news_pks(self, expanded_list: list[HashtagModel], keyword_pk_list: list[set[int]]) -> dict[str, list[int]]:
        result: dict[str, list[int]] = {}
        for expanded, keyword_pks in zip(expanded_list, keyword_pk_list):
            news_pks = await self._news_keyword_map_repository.find_news_fks_by_keyword_fks(list(keyword_pks))
            logger.debug("해시태그 검색: [%s, 뉴스 %d건]", expanded.hashtag, len(news_pks))
            result[expanded.hashtag] = news_pks
        return result
