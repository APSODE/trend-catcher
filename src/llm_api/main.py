import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.llm_api.core.logging import setup_logging
from src.llm_api.core.settings import get_settings
from src.llm_api.handler.exception_handler import register_exception_handlers
from src.llm_api.infrastructure.crawler_client import CrawlerClient
from src.llm_api.infrastructure.database import init_database
from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.infrastructure.user_api_client import UserApiClient
from src.llm_api.router import analysis_router, hashtag_router, news_router, scoring_router
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    http_client = httpx.AsyncClient()
    app.state.http_client = http_client
    app.state.nvidia_client = NvidiaClient(http_client, settings.nvidia_api_key)
    app.state.crawler_client = CrawlerClient(http_client, settings.crawler_api_url)
    app.state.user_api_client = UserApiClient(http_client, settings.user_api_url)

    await init_database()
    logger.info("llm api 구동시작")

    yield

    await http_client.aclose()
    logger.info("llm api 구동종료")

def create_app() -> FastAPI:
    setup_logging(get_settings().log_level)

    app = FastAPI(title = "LLM API", description = "뉴스 분석 및 해시태그 검색 API", lifespan = lifespan)
    register_exception_handlers(app)

    app.include_router(analysis_router.router)
    app.include_router(scoring_router.router)
    app.include_router(hashtag_router.router)
    app.include_router(news_router.router)

    return app

app = create_app()

