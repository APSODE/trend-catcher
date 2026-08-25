import logging

from datetime import datetime, date
from beanie import SortDirection, PydanticObjectId
from bson.errors import InvalidId

from src.crawler_api.constant.news_sitemap import NewsSitemap
from src.crawler_api.exception.create_error_exception import CreateErrorException
from src.crawler_api.exception.not_found_exception import NotFoundException
from src.crawler_api.repository.article_repository import ArticleRepository
from src.crawler_api.schemas.article import ArticleRead, ArticleCreate, ArticleUpdate, ArticleResponseSNS, \
    ArticleResponseLLM, ArticleResponseFront
from src.crawler_api.service.crawling_pipeline import CrawlingPipeline
from src.crawler_api.util.normalize_datetime import now_date


logger = logging.getLogger(__name__)

class ArticleService:
    def __init__(self, article_repository: ArticleRepository):
        self._article_repository = article_repository

    async def _filter_new_urls(self, urls: list[str]) -> list[str]:
        existing = await self._article_repository.exist_by_urls(urls)
        return [u for u in urls if u not in existing]

    async def get_all_articles(self) -> list[ArticleRead]:
        result: list[ArticleRead] = []

        for article in await self._article_repository.find_all(
                sort=[("crawled_at", SortDirection.DESCENDING), ("published_at", SortDirection.ASCENDING)]
        ):

            if article is not None:
                result.append(ArticleRead.model_validate(article))

        return result

    async def get_article_by_id(self, article_id: PydanticObjectId) -> ArticleRead:
        article = await self._article_repository.get_by_id(article_id)

        if article is None:
            raise NotFoundException("ID로 기사를 찾지 못했습니다")

        return ArticleRead.model_validate(article)

    async def get_article_by_date(self, datetime_value: datetime) -> list[ArticleRead]:
        result: list[ArticleRead] = []

        for article in await self._article_repository.get_by_date(date=datetime_value):
            if article is not None:
                result.append(ArticleRead.model_validate(article))

        return result
    async def get_article_by_date_llm(self, start_date: datetime, end_date: datetime) -> list[ArticleResponseLLM]:
        result: list[ArticleResponseLLM] = []

        for article in await self._article_repository.get_by_date_to_date(start_date=start_date, end_date=end_date):
            if article is not None:
                result.append(ArticleResponseLLM.model_validate(article))

        return result

    async def get_article_by_ids_sns(self, article_ids: list[str]) -> list[ArticleResponseSNS]:
        result: list[ArticleResponseSNS] = []

        ids: list[PydanticObjectId] = []
        for string in article_ids:
            try:
                ids.append(PydanticObjectId(string))
            except InvalidId:
                logger.warning("잘못된 ObjectId 형식: %s", string)

        for article in await self._article_repository.get_by_ids(ids):
            if article is not None:
                result.append(ArticleResponseSNS.model_validate(article))
        return result

    async def get_article_by_ids_front(self, article_ids: list[str]) -> list[ArticleResponseFront]:

        result: list[ArticleResponseFront] = []

        ids: list[PydanticObjectId] = []
        for string in article_ids:
            try:
                ids.append(PydanticObjectId(string))
            except InvalidId:
                logger.warning("잘못된 ObjectId 형식: %s", string)

        for article in await self._article_repository.get_by_ids(ids):
            if article is not None:
                result.append(ArticleResponseFront.model_validate(article))
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

    async def create_articles_today(
        self,
        sources: list[NewsSitemap] | None = None,
        limit: int | None = None
    ) -> list[PydanticObjectId]:

        if sources is None:
            sources = list(NewsSitemap)

        today_crawled_articles = await CrawlingPipeline.run_all_today(sources=sources, limit=limit)
        return await self.create_articles(today_crawled_articles)

    async def create_articles_dates(
        self,
        sources: list[NewsSitemap] | None = None,
        limit: int | None = None,
        dates: list[date] | None = None
    ) -> list[PydanticObjectId]:
        if dates is None:
            dates = [now_date()]

        if sources is None:
            sources = list(NewsSitemap)

        date_crawled_articles = await CrawlingPipeline.run_all(sources=sources, limit=limit, dates=dates)
        return await self.create_articles(date_crawled_articles)

    async def update_article(
        self,
        article_id: PydanticObjectId,
        article: ArticleUpdate
    ) -> ArticleRead:

        update_data = article.model_dump(exclude_unset=True, exclude_none=True)

        result = await self._article_repository.update_by_id(article_id, update_data)
        if result is None:
            raise NotFoundException("값을 찾을 수 없습니다")

        return ArticleRead.model_validate(result)

    async def delete_article(self, article_id: PydanticObjectId) -> bool:
        return await self._article_repository.delete_by_id(article_id)

    async def delete_all_articles(self, amount: int | None) -> bool:
        if amount is None:
            return await self._article_repository.delete(amount=0)

        return await self._article_repository.delete(amount=amount)
