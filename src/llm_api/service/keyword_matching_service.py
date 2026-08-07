from src.llm_api.constant.similarity_constant import SimilarityConstant
from src.llm_api.model.keyword_model import KeywordModel
from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.schema.keyword_query import KeywordQueryData
from src.llm_api.util.similarity_util import SimilarityUtil
import logging

logger = logging.getLogger(__name__)

class KeywordMatchingService:
    def __init__(self, keyword_repository: KeywordRepository):
        self._keyword_repository = keyword_repository

    #검색어와 키워드pk 매칭
    async def find_matching_pks(self, queries: list[KeywordQueryData]) -> list[set[int]]:
        #빈 리스트 방어
        if not queries:
            return []

        candidates = await self._keyword_repository.find_all()
        return [await self._match(query, candidates) for query in queries]

    #검색 하나 처리
    async def _match(self, query: KeywordQueryData, candidates: list[KeywordModel]) -> set[int]:
        exact_pks = await self._match_exact(query.terms) #정확히 맞는 매칭
        similar_pks = self._match_similar(query.embedding, candidates) #임베딩 기준 유사한 매칭
        return exact_pks | similar_pks #합집합

    #정확히 맞는 것들 매칭
    async def _match_exact(self, terms: list[str]) -> set[int]:
        matched = await self._keyword_repository.find_by_keywords(terms)
        return {keyword.pk for keyword in matched}

    #임베딩 기준 유사한 것들 매칭
    async def _match_similar(self, embedding: list[float], candidates: list[KeywordModel]) -> set[int]:
        matches = SimilarityUtil.find_similar_above(embedding, [candidate.embedding for candidate in candidates], SimilarityConstant.KEYWORD_MERGE_THRESHOLD)
        for index, score in matches:
            logger.debug("키워드 임베딩 매칭: [키워드: %s, 유사도: %.3f]", candidates[index].keyword, score) #이게 무슨의미인지? 어디 매칭되었는지만 알고 뭔지는 모르잖아
        return {candidates[index].pk for index, _ in matches}