from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.model.keyword_model import KeywordModel
from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.constant.nvidia_constant import EmbeddingInputType
from src.llm_api.constant.similarity_constant import SimilarityConstant
from src.llm_api.util.similarity_util import SimilarityUtil
import logging

logger = logging.getLogger(__name__)

class KeywordAssignmentService:
    def __init__(self, client: NvidiaClient, keyword_repository: KeywordRepository):
        self._client = client
        self._keyword_repository = keyword_repository

    async def assign(self, keywords: list[str]) -> list[KeywordModel]:
        keywords = list(dict.fromkeys(keywords))
        candidates = await self._keyword_repository.find_all()

        matched, unmatched = self._filter_already_exist(keywords, candidates)
        matched |= await self._resolve_unmatched(unmatched, candidates)

        return self._deduplicate(keywords, matched)

    #이미 있는 키워드들 필터링
    def _filter_already_exist(self, keywords: list[str], candidates: list[KeywordModel]) -> tuple[dict[str, KeywordModel], list[str]]:
        matched: dict[str, KeywordModel] = {}
        unmatched: list[str] = []

        for keyword in keywords:
            exact = KeywordAssignmentService._find_already_exist(keyword, candidates)
            if exact is not None:
                matched[keyword] = exact
            else:
                unmatched.append(keyword)
        return matched, unmatched

    #매칭 안된것들 일괄포장
    async def _resolve_unmatched(self, unmatched: list[str], candidates: list[KeywordModel]) -> dict[str, KeywordModel]:
        if not unmatched:
            return {}

        embeddings = await self._client.create_embeddings(unmatched, EmbeddingInputType.PASSAGE)

        resolved: dict[str, KeywordModel] = {}
        for keyword, embedding in zip(unmatched, embeddings):
            model = await self._match_or_create(keyword, embedding, candidates)
            resolved[keyword] = model
            if model not in candidates:
                candidates.append(model)
        return resolved

    #중복 제거
    def _deduplicate(self, keywords: list[str], matched: dict[str, KeywordModel]) -> list[KeywordModel]:
        unique: dict[int, KeywordModel] = {}
        for keyword in keywords:
            model = matched[keyword]
            unique.setdefault(model.pk, model)
        return list(unique.values())

    #이미 존재하는 키워드인지 파악
    @staticmethod
    def _find_already_exist(keyword: str, candidates: list[KeywordModel]) -> KeywordModel | None:
        return next((candidate for candidate in candidates if candidate.keyword == keyword), None)

    async def _match_or_create(self, keyword: str, embedding: list[float], candidates: list[KeywordModel]) -> KeywordModel:
        best_match = SimilarityUtil.find_most_similar(embedding, [candidate.embedding for candidate in candidates])
        if best_match is not None:
            best_match_index, best_match_similarity = best_match

            #기준점수 이상이면 그걸 리턴
            if best_match_similarity >= SimilarityConstant.KEYWORD_MERGE_THRESHOLD:
                logger.debug("키워드 매칭 성공: [keyword: %s, 편입된 키워드: %s, 유사도: %.3f]", keyword, candidates[best_match_index].keyword, best_match_similarity)
                return candidates[best_match_index]
            else:
                logger.debug("키워드 매칭 실패: [keyword: %s, 최고 유사 키워드: %s, 유사도: %.3f]", keyword,candidates[best_match_index].keyword, best_match_similarity)
        
        #아니면 새로 만듦
        logger.debug("신규 키워드 생성: %s", keyword)
        return await self._keyword_repository.create_keyword(keyword, embedding)