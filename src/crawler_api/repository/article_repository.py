from datetime import datetime, time

from beanie import PydanticObjectId, SortDirection
from pymongo.asynchronous.client_session import AsyncClientSession

from src.crawler_api.model.article import Article
from src.crawler_api.repository.base_repository import BaseRepository
from src.crawler_api.schemas.article import ArticleCreate, ArticleUpdate
from src.crawler_api.util.normalize_datetime import now_normalized


class ArticleRepository(BaseRepository[Article, PydanticObjectId]):
    def __init__(self, session : AsyncClientSession | None = None):
        super().__init__(Article, session)


    async def create_one(self, schema : ArticleCreate) -> PydanticObjectId | None:
        exist_data = await self.get_by_url(schema.url)
        if exist_data:
            update_date = schema.model_dump(exclude_unset = True, exclude_none= True)
            update_date["db_updated_at"] = now_normalized()
            await exist_data.set(update_date)
            return exist_data.id
        document = Article(**schema.model_dump())
        return await self.add_one(document)

    async def create_many(self, schemas : list[ArticleCreate]) -> list[PydanticObjectId]:
        ids : list[PydanticObjectId] = []
        schemas = list(filter(lambda x: x.url, schemas))

        for schema in schemas:
            exist_data = await self.get_by_url(schema.url)
            if exist_data:
                update_schema = (ArticleUpdate(**schema.model_dump()))
                update_data = update_schema.model_dump(exclude_unset=True, exclude_none=True)

                update_data["db_updated_at"] = now_normalized()
                await exist_data.set(update_data, session=self._session)
                if exist_data.id is not None:
                    ids.append(exist_data.id)

            else:
                document = Article(**schema.model_dump())
                result = await self.add_one(document)
                if result is not None:
                    ids.append(result)
        return ids

    async def get_by_url(self, url: str)  -> Article | None:
        return await self.find_one({"url": url})

    async def exists_by_url(self, url: str) -> bool:
        return await self.is_exist({"url": url})

    async def update_by_url(self, url: str, schema : ArticleUpdate) -> Article | None:
        update_data = schema.model_dump(exclude_unset = True, exclude_none= True)
        if not update_data:
            return None
        update_data["db_updated_at"] = now_normalized()

        result = await self.update({"url": url}, update_data = update_data)
        if result is None:
            return None
        return result[0]


    async def update_by_id(self, target_id : PydanticObjectId, update_date : dict) -> Article | None:
        if not update_date:
            return None
        update_date["db_updated_at"] = now_normalized()
        document = await self.get_by_id(target_id)

        if document is None:
            return None

        await document.set(update_date, session = self._session)
        return document



    async def get_by_company(
            self,
            company_name : str,
            amount : int = 0) -> list[Article]:
        return await self.find(
            {"company_name": company_name},
            amount = amount,
            sort = [("crawled_at", SortDirection.DESCENDING)])

    async def get_by_category(
            self,
            category : str,
            amount: int = 0) -> list[Article]:
        return await self.find(
            {"category": category},
            amount = amount,
            sort = [("crawled_at", SortDirection.DESCENDING)])

    async def get_by_date_to_date(self,
                          start_date : datetime,
                          end_date : datetime,
                          amount : int = 0) -> list[Article]:
        
        return await self.find(
            {"crawled_at": {"$gte" : start_date, "$lte" : end_date}},
            amount = amount,
            sort = [("crawled_at", SortDirection.DESCENDING)])


    async def get_by_date(self,
                          date : datetime,
                          amount : int = 0) -> list[Article]:
        start = datetime.combine(date.date(), time.min)
        return await self.get_by_date_to_date(start, date, amount)

    async def search_by_title(self,
                              keyword : str,
                              amount : int = 0) -> list[Article]:
        return await self.find(
            {"title": {"$regex": keyword, "$options": "i"}},
            amount = amount,
            sort = [("crawled_at", SortDirection.DESCENDING)]
        )