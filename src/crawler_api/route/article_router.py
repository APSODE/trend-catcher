from datetime import datetime
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query
from fastapi.openapi.models import Example

from src.crawler_api.dependencies.article import get_article_service
from src.crawler_api.schemas.article import ArticleRead, ArticleResponse, ArticleCreate, ArticleUpdate
from src.crawler_api.service.article_service import ArticleService
from src.crawler_api.util.normalize_datetime import normalize_datetime


router = APIRouter(
    prefix="/article",
    tags=["Article"],
)
@router.get("/articles", response_model=list[ArticleRead])
async def get_all_articles(service: ArticleService = Depends(get_article_service)):
    return await service.get_all_articles()


@router.post("/articles_today", response_model=list[PydanticObjectId])
async def get_articles_today(
    service: ArticleService = Depends(get_article_service),
    limit: int | None = None
):
    return await service.create_articles_today(None, limit=limit)

@router.get("/articles_date", response_model=list[ArticleResponse])
async def get_articles_by_date(
    datetime_value: datetime =
        Query(openapi_examples={
            "default": Example(
            summary="Example datetime value",
            value="1900-01-01T00:00:00")
        }),
    service: ArticleService = Depends(get_article_service)
):

    return await service.get_article_by_date(normalize_datetime(datetime_value))

@router.delete("/delete_all", response_model=bool)
async def delete_all_articles(
    service: ArticleService = Depends(get_article_service),
    amount: int | None = None
):

    return await service.delete_all_articles(amount=amount)


@router.get("/{article_id}", response_model=ArticleRead)
async def get_article(
        article_id: PydanticObjectId,
        service: ArticleService = Depends(get_article_service)
):

    return await service.get_article_by_id(article_id)

@router.post("/", response_model=PydanticObjectId, status_code=201)
async def create_article(
    article_data: ArticleCreate,
    service: ArticleService = Depends(get_article_service)
):

    return await service.create_article(article_data)
@router.delete("/{article_id}", response_model=bool)
async def delete_article(
    article_id: PydanticObjectId,
    service: ArticleService = Depends(get_article_service),
):

    return await service.delete_article(article_id)


@router.put("/{article_id}", response_model=ArticleRead)
async def update_article(
    article_id: PydanticObjectId,
    update_data: ArticleUpdate,
    service: ArticleService = Depends(get_article_service)
):

    return await service.update_article(article_id=article_id, article=update_data)
