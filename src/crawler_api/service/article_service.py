from datetime import datetime

from beanie import SortDirection, PydanticObjectId

from src.crawler_api.exception.create_error_exception import CreateErrorException
from src.crawler_api.exception.not_found_exception import NotFoundException
from src.crawler_api.repository.article_repository import ArticleRepository
from src.crawler_api.schemas.article import ArticleRead, ArticleResponse, ArticleCreate, ArticleUpdate


class ArticleService:
    def __init__(self, article_repository : ArticleRepository):
        self._article_repository = article_repository

    async def get_all_articles(self) -> list[ArticleRead]:
        result : list[ArticleRead] = []
        for article in await self._article_repository.find_all(sort = [("crawled_at", SortDirection.DESCENDING)]):
            if article is not None:
                result.append(ArticleRead.model_validate(article))

        return result

    async def get_article_by_id(self, article_id: PydanticObjectId) -> ArticleRead | None:
        article = await self._article_repository.get_by_id(article_id)

        if article is None:
            raise NotFoundException("ID로 기사를 찾지 못했습니다")

        return ArticleRead.model_validate(article)

    async def get_article_by_date(self, date: datetime) -> list[ArticleResponse]:
        result: list[ArticleResponse] = []
        for article in await self._article_repository.get_by_date(date = date):
            if article is not None:
                result.append(ArticleResponse.model_validate(article))
        return result

    async def create_article(self, article: ArticleCreate) -> PydanticObjectId:
        result = await self._article_repository.create_one(article)
        if result is None:
            raise CreateErrorException("생성 과정에서 오류가 발생했습니다")
        return result

    async def create_articles(self, articles: list[ArticleCreate]) -> list[PydanticObjectId]:
        if not articles:
            return []
        result = await self._article_repository.create_many(articles)
        if not result:
            return []
        return result

    async def update_article(self, article_id: PydanticObjectId, article: ArticleUpdate) -> ArticleRead:
        update_data = article.model_dump(exclude_unset=True, exclude_none=True)

        result = await self._article_repository.update_by_id(article_id, update_data)
        if result is None:
            raise NotFoundException("값을 찾을 수 없습니다")
        else:
            return ArticleRead.model_validate(result)

    async def delete_article(self, article_id: PydanticObjectId) -> bool:
        return await self._article_repository.delete_by_id(article_id)

    #권한 검증
    async def delete_all_articles(self, amount : int | None) -> bool:
        if amount is None:
            return await self._article_repository.delete(amount = 0)
        return await self._article_repository.delete(amount = amount)