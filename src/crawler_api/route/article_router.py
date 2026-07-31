from datetime import datetime, time, date

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from src.crawler_api.dependencies.article import get_article_service
from src.crawler_api.schemas.article import ArticleRead, ArticleResponse, ArticleCreate, ArticleUpdate
from src.crawler_api.service.article_service import ArticleService
from src.crawler_api.service.crawling_pipeline import CrawlingPipeline

router = APIRouter(
    prefix="/article",
    tags=["Article"],
)
@router.get("/articles", response_model = list[ArticleRead])
async def get_all_articles(
        service : ArticleService = Depends(get_article_service)
):
    return await service.get_all_articles()


@router.post("/articles_today", response_model = list[PydanticObjectId])
async def get_articles_today(
        service : ArticleService = Depends(get_article_service),
        limit : int | None = None):
    result = await CrawlingPipeline.run_all_today(None, limit=limit)
    return await service.create_articles(result)

@router.delete("/delete_all", response_model = bool)
async def delete_all_articles(
        service : ArticleService = Depends(get_article_service),
        amount : int | None = None
):
    return await service.delete_all_articles(amount = amount)
@router.get("/{date_value}/{time_value}", response_model=list[ArticleResponse])
async def get_articles_by_date(
        date_value: date,
        time_value : time,
        service : ArticleService = Depends(get_article_service)
):
    target_datetime = datetime.combine(date_value, time_value)
    return await service.get_article_by_date(target_datetime)

@router.get("/{article_id}", response_model=ArticleRead)
async def get_article(
        article_id: PydanticObjectId,
        service : ArticleService = Depends(get_article_service)
):
    return await service.get_article_by_id(article_id)

@router.post("/", response_model=PydanticObjectId, status_code=201)
async def create_article(
        article_data : ArticleCreate,
        service : ArticleService = Depends(get_article_service)
):
    return await service.create_article(article_data)
@router.delete("/{article_id}", response_model = bool)
async def delete_article(
        article_id: PydanticObjectId,
        service : ArticleService = Depends(get_article_service),
):
    return await service.delete_article(article_id)


@router.put("/{article_id}", response_model=ArticleRead)
async def update_article(
        article_id: PydanticObjectId,
        article_date : ArticleUpdate,
        service : ArticleService = Depends(get_article_service)
):
    return await service.update_article(article_id, article_date)

