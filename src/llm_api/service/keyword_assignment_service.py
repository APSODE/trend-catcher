from src.llm_api.model.keyword_model import KeywordModel
from src.llm_api.service.embedding_service import EmbeddingService
from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from sqlalchemy.ext.asyncio import AsyncSession


class KeywordAssignmentService:
    SIMILARITY_STANDARD = 0.9 #실험해보면서 조정 필요

    def __init__(self, keyword_repo: KeywordRepository, news_keyword_map_repo: NewsKeywordMapRepository, embedding_service: EmbeddingService):
        self.keyword_repo = keyword_repo
        self.news_keyword_map_repo = news_keyword_map_repo
        self.embedding_service = embedding_service

    async def assign_keywords(self, session: AsyncSession, news_id: int, keywords: list[str]) -> None:
        for target_keyword in keywords:
            keyword = await self.get_or_create_by_similarity(session, target_keyword)
            await self.news_keyword_map_repo.save(session, news_id, keyword.id)

    async def get_or_create_by_similarity(self, session: AsyncSession, keyword: str) -> KeywordModel:
        #동일한 키워드 있으면 바로 그거 리턴
        same_keyword = await self.keyword_repo.get(session, keyword)
        if same_keyword is not None:
            return same_keyword

        #없으면 임베딩 기반 검색 실시
        embedding = await self.embedding_service.get_embedding(keyword)
        keywordlist = await self.keyword_repo.get_all(session)

        for comprasion_keyword in keywordlist:
            similarity = self.embedding_service.get_similarity_score(embedding, comprasion_keyword.embedding)
            if similarity >= self.SIMILARITY_STANDARD:
                return comprasion_keyword

        #검색 결과도 없으면 새 키워드 생성
        new_keyword = await self.keyword_repo.create(session, keyword, embedding)
        return new_keyword