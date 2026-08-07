from src.llm_api.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.model.news_analysis_model import NewsAnalysisModel


class NewsAnalysisRepository(BaseRepository[NewsAnalysisModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NewsAnalysisModel)

    #분석된 뉴스인지 검색
    async def is_exist_by_crawled_id(self, crawled_id: str) -> bool:
        result = await self._find_one(NewsAnalysisModel.crawled_id == crawled_id)
        return result is not None

    #크롤러id로 검색
    async def find_by_crawled_id(self, crawled_id: str) -> NewsAnalysisModel | None:
        return await self._find_one(NewsAnalysisModel.crawled_id == crawled_id)

    #점수 없는애들 검색
    async def find_unscored(self, limit: int) -> list[NewsAnalysisModel]:
        stmt = self._select(NewsAnalysisModel.score.is_(None)).limit(limit)
        result = await self._session.scalars(stmt)
        return list(result.all())

    #점수 채우기
    async def update_score(self, news: NewsAnalysisModel, score: float, cross_check_score: float):
        news.score = score
        news.cross_check_score = cross_check_score
        await self._session.flush()

    #모델 포장
    async def create_analysis(self, crawled_id: str, category: str | None, topic_fk: int, content_score: float) -> NewsAnalysisModel:
        new_analysis = NewsAnalysisModel(crawled_id = crawled_id, category = category, topic_fk = topic_fk, content_score = content_score)
        return await self.save(new_analysis)

    #TODO: 알림용 이번 타임 뉴스만 반환 메소드 필요