from typing import AsyncGenerator
from fastapi import Depends, Request

from src.crawler_api.db.article_context import ArticleContext
from src.crawler_api.service.article_service import ArticleService



async def get_article_context(request: Request) -> AsyncGenerator[ArticleContext, None]:
    async with ArticleContext(request.app.state.mongo_client) as ctx:
        yield ctx

async def get_article_service(
    ctx: ArticleContext = Depends(get_article_context),
) -> ArticleService:

    return ArticleService(article_repository=ctx.articles)

#스케줄러용 service create
async def create_article_service(
    ctx: ArticleContext,
) -> ArticleService:

    return ArticleService(article_repository=ctx.articles)