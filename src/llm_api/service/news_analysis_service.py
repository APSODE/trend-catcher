from src.llm_api.model.news_analysis_model import NewsAnalysisModel
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.service.embedding_service import EmbeddingService
from src.llm_api.service.extraction_service import ExtractionService
from src.llm_api.service.reliability_service import ReliabilityService
from src.llm_api.service.topic_matching_service import TopicMatchingService
from src.llm_api.service.keyword_assignment_service import KeywordAssignmentService
from sqlalchemy.ext.asyncio import AsyncSession

class NewsAnalysisService:
    def __init__(self, news_analysis_repo: NewsAnalysisRepository, extraction_service: ExtractionService, embedding_service: EmbeddingService, topic_matching_service: TopicMatchingService, keyword_assignment_service: KeywordAssignmentService, reliability_service: ReliabilityService):
        self.news_analysis_repo = news_analysis_repo
        self.extraction_service = extraction_service
        self.embedding_service = embedding_service
        self.topic_matching_service = topic_matching_service
        self.keyword_assignment_service = keyword_assignment_service
        self.reliability_service = reliability_service

    #분석한다 뉴스: 크롤러 DICT를 그대로 받아 사용
    async def analyze_news(self, session: AsyncSession, news: dict) -> NewsAnalysisModel | None:
        news_id = news["id"]
        title = news["title"]
        content = news["content"]
        category = news["category"]

        #체크한다 이미 한 건지
        if await self.news_analysis_repo.is_exist(session, news_id):
            return None

        #추출한다 주제 그리고 키워드
        extracted_data = await self.extraction_service.extract(title, content)
        if extracted_data is None: #크레이지 AI 안 한다면 일 똑바로 쫓아낸다
            return None

        #한다 임베딩
        target_text = f"{title}. {extracted_data['topic']}"
        embedding = await self.embedding_service.get_embedding(target_text)

        #여기부턴 db 손대는 영역이라 try
        try:
            match_data = await self.topic_matching_service.create_topic_match_data(session, embedding, news_id, extracted_data["topic"])
            score = self.reliability_service.calculate_final_score(extracted_data["content_score"], match_data.main_topic_count)
            analysis = await self.news_analysis_repo.save(session, NewsAnalysisModel(news_id = news_id, category = category, topic_id = match_data.main_topic_id, score = score["score"], score_detail = score["score_detail"]))
            await self.topic_matching_service.save_topic_match_data(session, analysis.id, match_data)
            await self.keyword_assignment_service.assign_keywords(session, analysis.id, extracted_data["keywords"])
            await session.commit()
            return analysis
        except Exception:
            await session.rollback()
            raise

    #여러 개 받아서 처리
    async def analyze_news_list(self, session: AsyncSession, news_list: list[dict]) -> list[NewsAnalysisModel]:
        results = []
        for news in news_list:
            try:
                analysis = await self.analyze_news(session, news)
                if analysis is not None:
                    results.append(analysis)
            except Exception as e:
                print(f"처리 실패: news_id = {news.get('id')}, error = {e}")
        return results