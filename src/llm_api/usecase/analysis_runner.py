from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from src.llm_api.repository.topic_repository import TopicRepository
from src.llm_api.service.extraction_service import ExtractionService
from src.llm_api.service.keyword_assignment_service import KeywordAssignmentService
from src.llm_api.service.topic_matching_service import TopicMatchingService
from src.llm_api.constant.schedule_constant import ScheduleConstant
from src.llm_api.schema.article import CrawledArticleData
from src.llm_api.schema.analysis_result import AnalysisResultData
from src.llm_api.infrastructure.crawler_client import CrawlerClient
from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.util.datetime_util import DateTimeUtil
from src.llm_api.infrastructure.database import session_scope
from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.service.news_analysis_service import NewsAnalysisService
from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class AnalysisRunner:
    def __init__(self, crawler_client: CrawlerClient, nvidia_client: NvidiaClient):
        self._crawler_client = crawler_client
        self._nvidia_client = nvidia_client

    #메인동작
    async def run(self) -> AnalysisResultData:
        now = DateTimeUtil.get_now_kst()
        since = now - timedelta(hours = ScheduleConstant.FETCH_HOURS)
        articles = await self._crawler_client.get_articles(since, now)
        logger.info("분석 시작: %d건 수신 (%s ~ %s)", len(articles), since, now)
        return await self._analyze_each(articles)

    #여러개 받아서 하나씩 분석
    async def _analyze_each(self, articles: list[CrawledArticleData]) -> AnalysisResultData:
        result = AnalysisResultData()
        total = len(articles)

        for index, article in enumerate(articles, start = 1):
            try:
                analysis = await self._analyze_one(article)
            except Exception:
                logger.exception("분석 실패: [crawled_id: %s]", article.crawled_id)
                result.failed += 1
                continue
            else:
                if analysis is None:
                    result.skipped += 1
                else:
                    result.processed.append(analysis)
            finally:
                logger.info("진행: %d/%d", index, total)

        logger.info("분석 완료: [요청:%d건, 처리:%d건, 스킵:%d건, 실패:%d건]", len(articles), len(result.processed), result.skipped, result.failed)
        return result

    #한 건 분석: 독립 트랜잭션에서
    async def _analyze_one(self, article: CrawledArticleData) -> NewsAnalysisModel | None:
        async with session_scope() as session:
            service = self._build_service(session)
            return await service.analyze(article)

    #서비스 조합
    def _build_service(self, session: AsyncSession) -> NewsAnalysisService:
        return NewsAnalysisService(
            extraction_service = ExtractionService(self._nvidia_client),
            topic_matching_service = TopicMatchingService(self._nvidia_client, TopicRepository(session)),
            keyword_assignment_service = KeywordAssignmentService(self._nvidia_client, KeywordRepository(session)),
            news_analysis_repository = NewsAnalysisRepository(session),
            news_keyword_map_repository = NewsKeywordMapRepository(session)
        )