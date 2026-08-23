import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from src.sns_api.scheduler import create_scheduler

from src.sns_api.config import get_settings
from src.sns_api.handler.crawler_client import CrawlerClient
from src.sns_api.handler.discord_client import DiscordClient
from src.sns_api.handler.llm_client import LLMClient
from src.sns_api.handler.user_client import UserClient
from src.sns_api.router.subscription_router import router as subscription_router
from src.sns_api.router.dispatch_router import router as dispatch_router

settings = get_settings()

logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(timeout=settings.http_timeout_seconds) as http_client:
        app.state.discord_client = DiscordClient(http_client)
        app.state.user_client = UserClient(http_client)
        app.state.llm_client = LLMClient(http_client)
        app.state.crawler_client = CrawlerClient(http_client)

        scheduler = create_scheduler()

        if settings.enable_internal_scheduler:
            scheduler.start()

        yield

        if settings.enable_internal_scheduler:
            scheduler.shutdown()

app = FastAPI(title="SNS Service", version="0.1.0", lifespan=lifespan)

# 라우터 등록
app.include_router(subscription_router)
app.include_router(dispatch_router)

@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok", "service": settings.service_name}