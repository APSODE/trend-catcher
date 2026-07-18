from datetime import datetime

from beanie import PydanticObjectId
from fastapi import APIRouter

from src.crawler_api.schemas.article import ArticleRead, ArticleResponse, ArticleCreate

router = APIRouter(
    prefix="/article",
    tags=["Article"],
)

@router.get("/{article_id}", response_model=ArticleRead)
async def get_article(article_id: PydanticObjectId):
    #pass
    return ArticleRead(id=article_id, title="Test Article", content="Test Content", company_name="Test Company", crawled_at=datetime.now())

@router.get("/articles", response_model=list[ArticleRead])
async def get_all_articles():
    #pass
    return [{"id": "1", "title": "Test Article"}]

@router.get("{date}", response_model=list[ArticleResponse])
async def get_articles_by_date(date: datetime):
    return [{date.__str__(): "Test Article"}]

@router.post("/", response_model=ArticleRead, status_code=201)
async def create_article(article_data : ArticleCreate):
    pass

@router.delete("/{article_id}")
async def delete_article(article_id: str):
    pass

@router.put("/{article_id}", response_model=ArticleRead)
async def update_article(article_id: str):
    pass
