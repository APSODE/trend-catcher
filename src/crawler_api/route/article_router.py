from datetime import datetime, time, date

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from src.crawler_api.dependencies.article import get_article_service
from src.crawler_api.schemas.article import ArticleRead, ArticleResponse, ArticleCreate, ArticleUpdate
from src.crawler_api.service.article_service import ArticleService

router = APIRouter(
    prefix="/article",
    tags=["Article"],
)
@router.get("/articles", response_model=list[ArticleRead])
async def get_all_articles(
        service : ArticleService = Depends(get_article_service)
):
    return await service.get_all_articles()


@router.get("/{date}/{time}", response_model=list[ArticleResponse])
async def get_articles_by_date(
        date: date,
        time : time,
        service : ArticleService = Depends(get_article_service)
):
    target_datetime = datetime.combine(date, time)
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

#whitelist 미들웨어