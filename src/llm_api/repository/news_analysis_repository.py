from src.llm_api.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from datetime import datetime

class NewsAnalysisRepository(BaseRepository[NewsAnalysisModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, NewsAnalysisModel)

    #분석된 뉴스인지 검색
    async def is_exist_by_crawled_id(self, crawled_id: str) -> bool:
        result = await self._find_one(NewsAnalysisModel.crawled_id == crawled_id)
        return result is not None

    #점수 없는애들 검색
    async def find_unscored(self) -> list[NewsAnalysisModel]:
        stmt = self._select(NewsAnalysisModel.score.is_(None))
        result = await self._session.scalars(stmt)
        return list(result.all())

    #점수 채우기
    async def update_score(self, news: NewsAnalysisModel, score: float, cross_check_score: float):
        news.score = score
        news.cross_check_score = cross_check_score
        await self._session.flush()

    #모델 포장
    async def create_analysis(self, crawled_id: str, topic_fk: int, content_score: float) -> NewsAnalysisModel:
        new_analysis = NewsAnalysisModel(crawled_id = crawled_id, topic_fk = topic_fk, content_score = content_score)
        return await self.save(new_analysis)

    #기간 내 점수 있는 뉴스 리턴
    async def find_scored_between(self, since: datetime, until: datetime) -> list[NewsAnalysisModel]:
        return await self._find_all((NewsAnalysisModel.analyzed_at >= since) & (NewsAnalysisModel.analyzed_at < until) & NewsAnalysisModel.score.is_not(None))

    #pk 뉴스가 기간 내인지 필터
    async def find_scored_between_by_pks(self, pks: list[int], since: datetime, until: datetime) -> list[NewsAnalysisModel]:
        if not pks:
            return []
        return await self._find_all(NewsAnalysisModel.pk.in_(pks) & (NewsAnalysisModel.analyzed_at >= since) & (NewsAnalysisModel.analyzed_at < until) & NewsAnalysisModel.score.is_not(None))