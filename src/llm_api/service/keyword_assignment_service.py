from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.model.keyword_model import KeywordModel
from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.constant.scoring_constant import ScoringConstant
from src.llm_api.util.similarity_util import SimilarityUtil
import logging

logger = logging.getLogger(__name__)

class KeywordAssignmentService:
    def __init__(self, client: NvidiaClient, keyword_repository: KeywordRepository):
        self._client = client
        self._keyword_repository = keyword_repository

    async def assign(self, keywords: list[str]) -> list[KeywordModel]:
        keywords = list(dict.fromkeys(keywords)) #중복제거

        candidates = await self._keyword_repository.find_all()

        #완전히 겹치는 키워드들을 걸러냄
        result: dict[str, KeywordModel] = {}
        unmatched: list[str] = []
        for keyword in keywords:
            exact = self._find_already_exist(keyword, candidates)
            if exact is not None:
                result[keyword] = exact
            else:
                unmatched.append(keyword)

        #안겹치는 것들 임베딩
        if unmatched:
            embeddings = await self._client.create_embeddings(unmatched, "passage")

            #유사도 판정 후 적용
            for keyword, embedding in zip(unmatched, embeddings):
                model = await self._match_or_create(keyword, embedding, candidates)
                result[keyword] = model
                if model not in candidates:
                    candidates.append(model)

        #임베딩 뒤 중복 제거 후 순서 맞춰 리턴
        unique: dict[int, KeywordModel] = {}
        for keyword in keywords:
            model = result[keyword]
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
            if best_match_similarity >= ScoringConstant.KEYWORD_SIMILARITY_THRESHOLD:
                logger.debug("키워드 매칭 성공: [keyword: %s, 편입된 키워드: %s, 유사도: %.3f]", keyword, candidates[best_match_index].keyword, best_match_similarity)
                return candidates[best_match_index]
            else:
                logger.debug("키워드 매칭 실패: [keyword: %s, 최고 유사 키워드: %s, 유사도: %.3f]", keyword,candidates[best_match_index].keyword, best_match_similarity)
        
        #아니면 새로 만듦
        logger.info("신규 키워드 생성: %s", keyword)
        return await self._keyword_repository.create_keyword(keyword, embedding)