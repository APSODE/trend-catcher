from typing import TypeVar, Generic, Type, Mapping, Any

from beanie import Document, SortDirection, PydanticObjectId

ModelType = TypeVar("ModelType", bound = Document)

#검색용 객체
FilterType = TypeVar("FilterType", bound = Mapping[str, Any])
IdType = TypeVar("IdType", bound = PydanticObjectId)

class BaseRepository(Generic[ModelType, IdType]):
    def __init__(self, model_class : Type[ModelType]):
        self._model = model_class

    @property
    def model(self) -> Type[ModelType]:
        return self._model

    async def add_one(self, document : ModelType) -> IdType | None:
        await document.insert()
        return document.id

    async def add_many(self, documents : list[ModelType]) -> list[IdType]:
        if not documents:
            return []
        result = await self._model.insert_many(documents)
        return result.inserted_ids

    async def find(self,
                   filter_data : FilterType | None = None,
                   amount : int = 0,
                   sort : list[tuple[str, SortDirection]] | None = None) -> list[ModelType]:
        result = self._model.find(filter_data) if filter_data is not None else self._model.find_all()

        if sort:
            result = result.sort(sort)
        if amount > 0:
            result = result.limit(amount)
        return await result.to_list()

    async def find_one(self, filter_data : FilterType) -> ModelType | None:
        return await self._model.find_one(filter_data)

    async def find_all(self,
                       sort: list[tuple[str, SortDirection]] | None = None) -> list[ModelType]:
        return await self.find(sort = sort)

    async def get_by_id(self, data_id : IdType) -> ModelType | None:
        result = await self._model.get(data_id)
        return result


    async def update(self,
                     filter_data : FilterType,
                     update_data : dict) -> list[ModelType] | None:
        if not update_data:
            return None
        documents = await self._model.find(filter_data).to_list()
        await self._model.find(filter_data).update_many({"$set": update_data})
        return documents


    async def update_by_id(self,
                           target_id : IdType,
                           update_date : dict
                           ) -> ModelType | None:
        if not update_date:
            return None

        document = await self.get_by_id(target_id)

        if document is None:
            return None

        await document.set(update_date)
        return document

    async def delete(self,
                     filter_data: FilterType | None = None,
                      amount : int = 1) -> bool:
        query = self._model.find(filter_data) if filter_data else self._model.find_all()

        if amount == 1: #1건 삭제인경우
            document = await query.first_or_none()
            if document is None:
                return False
            else:
                await document.delete()

        else: #n건 삭제인 경우, 갯수 지정된 경우 갯수만큼 삭제
            documents = await query.to_list() if amount is None else await query.limit(amount).to_list()
            for document in documents:
                await document.delete()
            if len(documents) <= 0:
                return False
        return True

    async def delete_by_id(self, target_id : IdType) -> bool:
        document = await self.get_by_id(target_id)
        if document is None:
            return False

        await document.delete()
        return True

    async def is_exist(self, filter_data : FilterType) -> bool:
        result = await self._model.find(filter_data).limit(1).to_list()
        return len(result) > 0


    #TODO Session 관리