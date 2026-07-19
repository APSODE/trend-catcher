from sqlalchemy.ext.asyncio import AsyncSession
from model.news_analysis_model import NewsAnalysisModel
from sqlalchemy import select


class NewsAnalysisRepository:
    #새 뉴스 추가
    async def save(self, session: AsyncSession, news_analysis: NewsAnalysisModel) -> NewsAnalysisModel:
        session.add(news_analysis)
        await session.flush()
        return news_analysis

    #분석여부 확인
    async def is_exist(self, session: AsyncSession, target_id: str)-> bool:
        query = select(NewsAnalysisModel).where(NewsAnalysisModel.news_id == target_id)
        result = await session.execute(query)
        return result.scalar_one_or_none() is not None

    #주요 뉴스 반환: 커트라인 점수 이상인 뉴스 중 상위 n개
    async def get_main_news(self, session: AsyncSession, cutoff_score: float, limit: int) -> list[NewsAnalysisModel]:
        query = select(NewsAnalysisModel).where(NewsAnalysisModel.score >= cutoff_score).order_by(NewsAnalysisModel.score.desc()).limit(limit)
        result = await session.execute(query)
        return list(result.scalars().all())