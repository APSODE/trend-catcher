from datetime import datetime, date
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query

from src.crawler_api.dependencies.article import get_article_service
from src.crawler_api.schemas.article import ArticleRead, ArticleCreate, ArticleUpdate, ArticleResponseLLM, \
    ArticleResponseSNS, ArticleResponseFront
from src.crawler_api.service.article_service import ArticleService
from src.crawler_api.util.normalize_datetime import normalize_datetime


router = APIRouter(
    prefix="/article",
    tags=["Article"],
)

@router.post("/", response_model=PydanticObjectId, status_code=201)
async def create_article(
    article_data: ArticleCreate,
    service: ArticleService = Depends(get_article_service)
):
    return await service.create_article(article_data)

@router.post("/articles_today", response_model=list[PydanticObjectId])
async def create_articles_today(
    service: ArticleService = Depends(get_article_service),
    limit: int | None = None
):
    return await service.create_articles_today(None, limit=limit)

@router.post("/articles_date", response_model=list[PydanticObjectId])
async def create_articles_by_date(
    dates: list[date] =
        Query(json_schema_extra={
            "example": ["2000-01-01"],
            "items": {"type": "string", "examples": ["2000-01-01"]}
        }),

    service: ArticleService = Depends(get_article_service),
    limit: int | None = None
):
    return await service.create_articles_dates(dates=dates, limit=limit)

@router.get("/articles", response_model=list[ArticleRead])
async def get_all_articles(service: ArticleService = Depends(get_article_service)):
    return await service.get_all_articles()
@router.get("/articles_date", response_model=list[ArticleRead])
async def get_articles_by_date(
    datetime_value: datetime =
        Query(json_schema_extra={
            "example": "2000-01-01T00:00:00",
            "items": {"type": "string", "examples": "2000-01-01T:00:00:00"}
        }),

    service: ArticleService = Depends(get_article_service)
):
    return await service.get_article_by_date(normalize_datetime(datetime_value))


@router.get("/articles_date_llm", response_model=list[ArticleResponseLLM])
async def get_articles_by_dates_llm(
    start_date: datetime =
        Query(json_schema_extra={
            "example": "2000-01-01T00:00:00",
            "items": {"type": "string", "examples": "2000-01-01T:00:00:00"}
        }),

    end_date: datetime =
        Query(json_schema_extra={
            "example": "2000-01-01T00:00:00",
            "items": {"type": "string", "examples": "2000-01-01T:23:59:59"}
        }),

    service: ArticleService = Depends(get_article_service),
):
    return await service.get_article_by_date_llm(start_date=start_date, end_date=end_date)

@router.get("/articles_ids_sns", response_model=list[ArticleResponseSNS])
async def get_articles_by_ids_sns(
    article_ids: list[str] =
        Query(json_schema_extra={
            "example": ["5eb7cf5a86d9755df3a6c593"],
            "items": {"type": "string", "examples": ["5eb7cf5a86d9755df3a6c593"]}
        }),

    service: ArticleService = Depends(get_article_service),
):

    return await service.get_article_by_ids_sns(article_ids)

@router.get("/articles_ids_front", response_model=list[ArticleResponseFront])
async def get_articles_by_ids_front(
    article_ids: list[str] =
        Query(json_schema_extra={
            "example": ["5eb7cf5a86d9755df3a6c593"],
            "items": {"type": "string", "examples": ["5eb7cf5a86d9755df3a6c593"]}
        }),

    service: ArticleService = Depends(get_article_service),
):

    return await service.get_article_by_ids_front(article_ids)

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

@router.put("/{article_id}", response_model=ArticleRead)
async def update_article(
    article_id: PydanticObjectId,
    update_data: ArticleUpdate,
    service: ArticleService = Depends(get_article_service)
):

    return await service.update_article(article_id=article_id, article=update_data)

@router.delete("/{article_id}", response_model=bool)
async def delete_article(
    article_id: PydanticObjectId,
    service: ArticleService = Depends(get_article_service),
):

    return await service.delete_article(article_id)


