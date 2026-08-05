from src.llm_api.repository.base_repository import AbstractBaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.model.news_keyword_map_model import NewsKeywordMapModel
from sqlalchemy import select

class NewsKeywordMapRepository(AbstractBaseRepository[NewsKeywordMapModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NewsKeywordMapModel)

    #키워드로 뉴스 검색
    async def find_news_fks_by_keyword_fks(self, keyword_fks: list[int]) -> list[int]:
        if not keyword_fks: #빈 리스트 들어와서 터지는거 방지
            return []

        stmt = select(NewsKeywordMapModel.news_fk).where(NewsKeywordMapModel.keyword_fk.in_(keyword_fks)).distinct()
        result = await self._session.scalars(stmt)
        return list(result.all())

    # 모델 포장
    async def create_maps(
        self, news_fk: int, keyword_fks: list[int]) -> list[NewsKeywordMapModel]:
        models = [NewsKeywordMapModel(news_fk=news_fk, keyword_fk=fk) for fk in keyword_fks]
        return await self.save_all(models)
