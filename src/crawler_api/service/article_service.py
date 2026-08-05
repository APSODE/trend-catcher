from datetime import datetime

from beanie import SortDirection, PydanticObjectId

from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.event.event_publisher import EventPublisher
from src.crawler_api.event.event_types import EventType, DomainEvent
from src.crawler_api.exception.create_error_exception import CreateErrorException
from src.crawler_api.exception.not_found_exception import NotFoundException
from src.crawler_api.repository.article_repository import ArticleRepository
from src.crawler_api.schemas.article import ArticleRead, ArticleResponse, ArticleCreate, ArticleUpdate
from src.crawler_api.service.crawling_pipeline import CrawlingPipeline


class ArticleService:
    def __init__(self, article_repository : ArticleRepository, event_publisher : EventPublisher):
        self._article_repository = article_repository
        self._event_publisher = event_publisher

    async def get_all_articles(self) -> list[ArticleRead]:
        result : list[ArticleRead] = []
        for article in await self._article_repository.find_all(sort = [("crawled_at", SortDirection.DESCENDING)]):
            if article is not None:
                result.append(ArticleRead.model_validate(article))

        return result

    async def get_article_by_id(self, article_id: PydanticObjectId) -> ArticleRead:
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

        await self._event_publisher.publish(DomainEvent(
            entity = "Article",
            event_type = EventType.CREATED,
            entity_id = str(result),
            payload = article.model_dump()))

        return result

    async def create_articles(self, articles: list[ArticleCreate]) -> list[PydanticObjectId]:
        if not articles:
            return []
        result = await self._article_repository.create_many(articles)
        if not result:
            return []

        for article_id in result:
            await self._event_publisher.publish(DomainEvent(
                entity = "Article",
                event_type = EventType.CREATED,
                entity_id = str(article_id)))

        return result

    async def create_articles_today(self, sources : list[NewsSitemap] | None = None, limit : int | None = None) -> list[PydanticObjectId]:
        if sources is None:
            sources = list(NewsSitemap)
        today_crawled_articles = await CrawlingPipeline.run_all_today(sources = sources, limit=limit)
        return await self.create_articles(today_crawled_articles)

    async def update_article(self, article_id: PydanticObjectId, article: ArticleUpdate) -> ArticleRead:
        update_data = article.model_dump(exclude_unset=True, exclude_none=True)

        result = await self._article_repository.update_by_id(article_id, update_data)
        if result is None:
            raise NotFoundException("값을 찾을 수 없습니다")

        await self._event_publisher.publish(DomainEvent(
            entity = "Article",
            event_type = EventType.UPDATED,
            entity_id = str(article_id),
            payload = update_data))

        return ArticleRead.model_validate(result)

    async def delete_article(self, article_id: PydanticObjectId) -> bool:
        result = await self._article_repository.delete_by_id(article_id)

        if result:
            await self._event_publisher.publish(DomainEvent(
                entity = "Article",
                event_type = EventType.DELETED,
                entity_id = str(article_id)))
        return result

    #권한 검증
    async def delete_all_articles(self, amount : int | None) -> bool:
        if amount is None:
            return await self._article_repository.delete(amount = 0)
        return await self._article_repository.delete(amount = amount)


