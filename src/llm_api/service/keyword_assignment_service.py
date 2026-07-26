from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from sqlalchemy.ext.asyncio import AsyncSession


class KeywordAssignmentService:
    def __init__(self, keyword_repo: KeywordRepository, news_keyword_map_repo: NewsKeywordMapRepository):
        self.keyword_repo = keyword_repo
        self.news_keyword_map_repo = news_keyword_map_repo

    async def assign_keywords(self, session: AsyncSession, news_id: int, keywords: list[str]) -> None:
        for target_keyword in keywords:
            keyword = await self.keyword_repo.get_or_create(session, target_keyword)
            await self.news_keyword_map_repo.save(session, news_id, keyword.id)