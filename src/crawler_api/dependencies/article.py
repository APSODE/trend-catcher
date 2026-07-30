from src.crawler_api.repository.article_repository import ArticleRepository
from src.crawler_api.service.article_service import ArticleService


def get_article_service() -> ArticleService:
    repository = ArticleRepository()
    return ArticleService(repository)