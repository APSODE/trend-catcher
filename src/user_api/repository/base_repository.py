from typing import Generic, List, Optional, Type, TypeVar, Sequence
from sqlalchemy.sql.elements import ColumnElement
from src.user_api.db import DatabaseController, RelationPath
from src.user_api.model import BaseModel

ModelType = TypeVar("ModelType", bound = BaseModel)


class BaseRepository(Generic[ModelType]):
    def __init__(self, db_controller: DatabaseController, model_class: Type[ModelType]):
        self._db_controller = db_controller
        self._model_class = model_class

    @property
    def model_class(self) -> Type[ModelType]:
        return self._model_class

    @property
    def db_controller(self) -> DatabaseController:
        return self._db_controller


    async def add_data(self,
                       new_data: ModelType | List[ModelType],
                       with_flush: bool = False) -> None:
        await self.db_controller.add(new_data, with_flush)

    async def find(self,
                   filter: Optional[ColumnElement[bool]] = None,
                   load_relations: Optional[Sequence[RelationPath]] = None,
                   amount: int = 0) -> List[ModelType]:
        return await self._db_controller.get(
            model_class = self._model_class,
            filter = filter,
            load_relations = load_relations,
            amount = amount
        )

    async def find_one(self,
                       filter: Optional[ColumnElement[bool]] = None,
                       load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[ModelType]:
        results = await self.find(filter, load_relations, amount = 1)
        return results[0] if results else None

    async def find_all(self,
                       filter: Optional[ColumnElement[bool]] = None,
                       load_relations: Optional[Sequence[RelationPath]] = None) -> List[ModelType]:
        return await self.find(filter, load_relations)

    async def get_by_pk(self,
                        target_pk: int,
                        load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[ModelType]:
        return await self.find_one(
            filter = self._model_class.pk == target_pk,
            load_relations = load_relations
        )

    async def update(self,
                     filter: ColumnElement[bool],
                     update_data: dict,
                     with_flush: bool = False) -> None:
        await self._db_controller.update(
            self._model_class,
            update_data = update_data,
            filter = filter,
            with_flush = with_flush,
        )

    async def update_by_pk(self,
                           target_pk: int,
                           update_data: dict,
                           with_flush: bool = False) -> None:

        await self.update(filter = self._model_class.pk == target_pk,
                          update_data = update_data,
                          with_flush = with_flush)

    async def delete(self,
                     filter: Optional[ColumnElement[bool]] = None,
                     load_relations: Optional[Sequence[RelationPath]] = None,
                     amount: int = 1,
                     with_flush: bool = False) -> None:
        await self._db_controller.delete(
            self._model_class,
            filter = filter,
            amount = amount,
            load_relations = load_relations,
            with_flush = with_flush
        )

    async def delete_by_pk(self,
                           target_pk: int,
                           load_relations: Optional[Sequence[RelationPath]] = None,
                           with_flush: bool = False) -> None:
        await self.delete(
            filter =self._model_class.pk == target_pk,
            load_relations = load_relations,
            amount = 1,
            with_flush = with_flush,
        )

    async def is_exist(self,
                       filter: ColumnElement[bool],
                       load_relations: Optional[Sequence[RelationPath]] = None) -> bool:
        results = await self._db_controller.get(
            model_class = self._model_class,
            filter = filter,
            load_relations = load_relations,
            amount = 1
        )
        return len(results) > 0

