from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.sql.elements import ColumnElement

from src.user_api.db.db_controller import DatabaseController
from src.user_api.model.base_model import BaseModel

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


    async def add_data(self, new_data: ModelType | List[ModelType],with_commit: bool = False) -> None:
        await self.db_controller.add(new_data, with_commit)

    async def find(self, filter: Optional[ColumnElement[bool]] = None, amount: int = 0) -> List[ModelType]:
        return await self._db_controller.get(self._model_class, filter = filter, amount = amount)

    async def find_one(self, filter: ColumnElement[bool]) -> Optional[ModelType]:
        results = await self.find(filter, amount = 1)
        return results[0] if results else None

    async def find_all(self, filter: ColumnElement[bool]) -> List[ModelType]:
        return await self.find(filter)

    async def get_by_id(self, target_id: int) -> Optional[ModelType]:
        return await self.find_one(filter = self._model_class.id == target_id)

    async def update(
            self,
            filter: ColumnElement[bool],
            update_data: dict,
            with_commit: bool = False,
    ) -> None:
        await self._db_controller.update(
            self._model_class,
            update_data = update_data,
            filter = filter,
            with_commit = with_commit,
        )

    async def update_by_id(self, target_id: int, update_data: dict, with_commit: bool = False) -> None:
        await self.update(
            filter = self._model_class.id == target_id,
            update_data = update_data,
            with_commit = with_commit,
        )

    async def delete(
            self,
            filter: Optional[ColumnElement[bool]] = None,
            amount: int = 1,
            with_commit: bool = False,
    ) -> None:
        await self._db_controller.delete(
            self._model_class,
            filter = filter,
            amount = amount,
            with_commit = with_commit,
        )

    async def delete_by_id(self, target_id: int, with_commit: bool = False) -> None:
        await self.delete(
            filter = self._model_class.id == target_id,
            amount = 1,
            with_commit = with_commit,
        )

    async def is_exist(self, filter: ColumnElement[bool]) -> bool:
        results = await self._db_controller.get(self._model_class, filter = filter, amount = 1)
        return len(results) > 0

