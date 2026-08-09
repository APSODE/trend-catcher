from datetime import datetime, time
from beanie import PydanticObjectId, SortDirection
from pymongo import ReturnDocument, UpdateOne
from pymongo.asynchronous.client_session import AsyncClientSession

from src.crawler_api.model.article import Article
from src.crawler_api.repository.base_repository import BaseRepository
from src.crawler_api.schemas.article import ArticleCreate, ArticleUpdate
from src.crawler_api.util.normalize_datetime import now_normalized


class ArticleRepository(BaseRepository[Article, PydanticObjectId]):
    def __init__(self, session: AsyncClientSession | None = None):
        super().__init__(Article, session)

    async def create_one(self, schema: ArticleCreate) -> PydanticObjectId | None:
        now_time = now_normalized()
        update_data = ArticleUpdate(**schema.model_dump()).model_dump(exclude_none=True)

        collection = self._model.get_pymongo_collection()

        result = await collection.find_one_and_update(
            filter={"url" : schema.url},
            update=[{
                "$set": {
                    **update_data,

                    "crawled_at": {
                        "$cond": {
                            "if": { "$eq": [{ "$type": "$_id" }, "missing"] },
                            "then": schema.crawled_at,
                            "else": "$crawled_at"
                        }
                    },
                    "db_updated_at": {
                        "$cond": {
                            "if": { "$eq": [{ "$type": "$_id" }, "missing"] },
                            "then": "$$REMOVE",
                            "else": now_time
                        }
                    }
                }
            }],
            upsert=True,
            session=self._session,
            projection={"_id": 1},
            return_document=ReturnDocument.AFTER
        )
        return PydanticObjectId(result["_id"]) if result else None

    async def create_many(self, schemas: list[ArticleCreate]) -> list[PydanticObjectId]:
        schemas = [schema for schema in schemas if schema.url]
        if not schemas:
            return []

        now_time = now_normalized()
        operations = []

        for schema in schemas:
            update_data = ArticleUpdate(**schema.model_dump()).model_dump(exclude_none=True)

            operations.append(
                UpdateOne(
                    filter={"url": schema.url},
                    update=[{
                        "$set": {
                            **update_data,

                            "crawled_at": {
                                "$cond": {
                                    "if": { "$eq": [{ "$type": "$_id" }, "missing"] },
                                    "then": schema.crawled_at,
                                    "else": "$crawled_at"
                                }
                            },
                            "db_updated_at": {
                                "$cond": {
                                    "if": { "$eq": [{ "$type": "$_id" }, "missing"] },
                                    "then": "$$REMOVE",
                                    "else": now_time
                                }
                            }
                        }
                    }],
                    upsert=True,
                )
            )

        # UpdateOne 객체 모아서 한번에 삽입/갱신
        collection = self._model.get_pymongo_collection()
        await collection.bulk_write(operations, session=self._session, ordered=False)

        #PK를 return할 방법이 없음 -> 재조회
        urls = [schema.url for schema in schemas]
        cursor = collection.find(
            {"url": {"$in": urls}},
            projection={"_id": 1},
            session=self._session
        )
        docs = await cursor.to_list()
        return [PydanticObjectId(doc["_id"]) for doc in docs]


    async def get_by_url(self, url: str)  -> Article | None:
        return await self.find_one({"url": url})

    async def exists_by_url(self, url: str) -> bool:
        return await self.is_exist({"url": url})

    async def update_by_url(self, url: str, schema: ArticleUpdate) -> Article | None:
        update_data = schema.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            return None

        update_data["db_updated_at"] = now_normalized()

        result = await self.update({"url": url}, update_data=update_data)
        if result is None:
            return None
        return result[0]


    async def update_by_id(
        self,
        target_id: PydanticObjectId,
        update_data: dict
    ) -> Article | None:

        if not update_data:
            return None

        update_data["db_updated_at"] = now_normalized()
        document = await self.get_by_id(target_id)

        if document is None:
            return None

        await document.set(update_data, session=self._session)
        return document



    async def get_by_company(
        self,
        company_name: str,
        amount: int = 0
    ) -> list[Article]:

        return await self.find(
            filter_data={"company_name": company_name},
            amount=amount,
            sort=[("crawled_at", SortDirection.DESCENDING)]
        )

    async def get_by_category(
        self,
        category : str,
        amount: int = 0
    ) -> list[Article]:

        return await self.find(
            filter_data={"category": category},
            amount=amount,
            sort=[("crawled_at", SortDirection.DESCENDING)]
        )

    async def get_by_date_to_date(
        self,
        start_date: datetime,
        end_date: datetime,
        amount: int = 0
    ) -> list[Article]:
        
        return await self.find(
            filter_data={"crawled_at": {"$gte": start_date, "$lte": end_date}},
            amount=amount,
            sort=[("crawled_at", SortDirection.DESCENDING)]
        )


    async def get_by_date(
        self,
        date: datetime,
        amount: int = 0
    ) -> list[Article]:

        start = datetime.combine(date.date(), time.min)
        return await self.get_by_date_to_date(start, date, amount)

    async def search_by_title(
        self,
        keyword: str,
        amount: int = 0
    ) -> list[Article]:

        return await self.find(
            filter_data={"title": {"$regex": keyword, "$options": "i"}},
            amount=amount,
            sort=[("crawled_at", SortDirection.DESCENDING)]
        )