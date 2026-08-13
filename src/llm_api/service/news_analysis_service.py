from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from src.llm_api.schema.article import CrawledArticleData
from src.llm_api.service.extraction_service import ExtractionService
from src.llm_api.service.keyword_assignment_service import KeywordAssignmentService
from src.llm_api.service.topic_matching_service import TopicMatchingService
from src.llm_api.schema.analysis_result import AnalysisResultData
import logging

logger = logging.getLogger(__name__)

class NewsAnalysisService:
    def __init__(
        self,
        extraction_service: ExtractionService,
        topic_matching_service: TopicMatchingService,
        keyword_assignment_service: KeywordAssignmentService,
        news_analysis_repository: NewsAnalysisRepository,
        news_keyword_map_repository: NewsKeywordMapRepository
    ):
        self._extraction_service = extraction_service
        self._topic_matching_service = topic_matching_service
        self._keyword_assignment_service = keyword_assignment_service
        self._news_analysis_repository = news_analysis_repository
        self._news_keyword_map_repository = news_keyword_map_repository

    #기사 하나 분석
    async def analyze(self, news: CrawledArticleData) -> NewsAnalysisModel | None:
        #분석된 기사면 스킵
        if await self._news_analysis_repository.is_exist_by_crawled_id(news.crawled_id):
            logger.info("분석된 기사 스킵: %s", news.crawled_id)
            return None

        #주제, 키워드, 점수 추출
        extraction = await self._extraction_service.extract(news.title, news.content)

        #주제 적용
        topic = await self._topic_matching_service.match_or_create(extraction.topic, news.crawled_id)

        #키워드 적용
        keywords = await self._keyword_assignment_service.assign(extraction.keywords)

        #결과 저장
        analysis = await self._news_analysis_repository.create_analysis(news.crawled_id, topic.pk, extraction.content_score)

        #뉴스-키워드 연결
        await self._news_keyword_map_repository.create_maps(analysis.pk, [keyword.pk for keyword in keywords])
        logger.info("분석 완료: [crawled_id: %s, topic_pk: %d, keywords: %d]", news.crawled_id, topic.pk, len(keywords))
        return analysis

    #기사 여럿 분석: 실패한 건 로그남기고 건너뜀
    async def analyze_all(self, news_list: list[CrawledArticleData]) -> AnalysisResultData:
        result = AnalysisResultData()

        for news in news_list:
            try:
                analysis = await self.analyze(news)
            except Exception:
                logger.exception("분석 실패: [crawled_id: %s]", news.crawled_id)
                result.failed += 1
                continue

            if analysis is None:
                result.skipped += 1
            else:
                result.processed.append(analysis)


        logger.info("다중 분석 완료: 요청 %d건 중 %d건 완료, %d건 스킵, %d건 실패", len(news_list), len(result.processed), result.skipped, result.failed)
        return result