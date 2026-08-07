from typing import AsyncGenerator
from fastapi import Depends, Request

from src.crawler_api.db.article_context import ArticleContext
from src.crawler_api.event.event_publisher import EventPublisher
from src.crawler_api.service.article_service import ArticleService


def get_event_publisher(request: Request) -> EventPublisher:
    return request.app.state.event_publisher

async def get_article_context(request: Request) -> AsyncGenerator[ArticleContext, None]:
    async with ArticleContext(request.app.state.mongo_client) as ctx:
        yield ctx

async def get_article_service(
    ctx: ArticleContext = Depends(get_article_context),
    event_publisher: EventPublisher = Depends(get_event_publisher)
) -> ArticleService:

    return ArticleService(article_repository=ctx.articles, event_publisher=event_publisher)

#스케줄러용 service create
async def create_article_service(
    ctx: ArticleContext,
    event_publisher: EventPublisher
) -> ArticleService:

    return ArticleService(article_repository=ctx.articles, event_publisher=event_publisher)