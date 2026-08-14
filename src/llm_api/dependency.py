from fastapi import Request, Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.infrastructure.crawler_client import CrawlerClient
from src.llm_api.infrastructure.user_api_client import UserApiClient
from src.llm_api.infrastructure.database import get_session
from src.llm_api.service.scoring_service import ScoringService
from src.llm_api.repository.news_analysis_repository import NewsAnalysisRepository
from src.llm_api.repository.topic_repository import TopicRepository
from src.llm_api.service.major_news_service import MajorNewsService
from src.llm_api.service.hashtag_search_service import HashtagSearchService
from src.llm_api.service.hashtag_expansion_service import HashtagExpansionService
from src.llm_api.repository.hashtag_repository import HashtagRepository
from src.llm_api.service.keyword_matching_service import KeywordMatchingService
from src.llm_api.repository.keyword_repository import KeywordRepository
from src.llm_api.repository.news_keyword_map_repository import NewsKeywordMapRepository
from src.llm_api.usecase.analysis_runner import AnalysisRunner
from src.llm_api.usecase.hashtag_preparer import HashtagPreparer

#인프라
def get_nvidia_client(request: Request) -> NvidiaClient:
    return request.app.state.nvidia_client

def get_crawler_client(request: Request) -> CrawlerClient:
    return request.app.state.crawler_client

def get_user_api_client(request: Request) -> UserApiClient:
    return request.app.state.user_api_client

SessionDep = Annotated[AsyncSession, Depends(get_session)]
NvidiaClientDep = Annotated[NvidiaClient, Depends(get_nvidia_client)]
CrawlerClientDep = Annotated[CrawlerClient, Depends(get_crawler_client)]
UserApiClientDep = Annotated[UserApiClient, Depends(get_user_api_client)]

#서비스
def get_scoring_service(session: SessionDep) -> ScoringService:
    return ScoringService(NewsAnalysisRepository(session), TopicRepository(session))

def get_major_news_service(session: SessionDep) -> MajorNewsService:
    return MajorNewsService(NewsAnalysisRepository(session))

def get_hashtag_search_service(session: SessionDep, client: NvidiaClientDep) -> HashtagSearchService:
    return HashtagSearchService(
        expansion_service = HashtagExpansionService(client, HashtagRepository(session)),
        keyword_matching_service = KeywordMatchingService(KeywordRepository(session)),
        news_keyword_map_repository = NewsKeywordMapRepository(session),
        news_analysis_repository = NewsAnalysisRepository(session)
    )

ScoringServiceDep = Annotated[ScoringService, Depends(get_scoring_service)]
MajorNewsServiceDep = Annotated[MajorNewsService, Depends(get_major_news_service)]
HashtagSearchServiceDep = Annotated[HashtagSearchService, Depends(get_hashtag_search_service)]

#유스케이스
def get_analysis_runner(crawler_client: CrawlerClientDep, nvidia_client: NvidiaClientDep) -> AnalysisRunner:
    return AnalysisRunner(crawler_client, nvidia_client)

def get_hashtag_preparer(user_api_client: UserApiClientDep, nvidia_client: NvidiaClientDep) -> HashtagPreparer:
    return HashtagPreparer(user_api_client, nvidia_client)

AnalysisRunnerDep = Annotated[AnalysisRunner, Depends(get_analysis_runner)]
HashtagPreparerDep = Annotated[HashtagPreparer, Depends(get_hashtag_preparer)]