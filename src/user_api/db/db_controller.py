from collections.abc import Iterable
from typing import List, Optional, Type, TypeVar, Any, Dict

from sqlalchemy import select, update, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement

from src.user_api.model.base_model import BaseModel

ModelType = TypeVar("ModelType", bound = BaseModel)


class DatabaseController:
    def __init__(self, session: AsyncSession):
        self.__session = session

    @staticmethod
    def create_object(session: AsyncSession) -> "DatabaseController":
        return DatabaseController(session = session)

    @property
    def session(self) -> AsyncSession:
        return self.__session


    def __build_select(self, model_class: ModelType | Type[ModelType], filter: Optional[ColumnElement[bool]] = None) -> Select[tuple[Any]]:
        statement = select(model_class)

        if filter is not None:
            statement = statement.where(filter)


        return statement

    async def add(self, model: ModelType | Iterable[ModelType], with_commit: bool = False) -> None:
        if isinstance(model, Iterable):
            self.__session.add_all(model)

        else:
            self.__session.add(model)

        if with_commit:
            await self.commit()


    async def get(self,
                  model_class: ModelType | Type[ModelType],
                  filter: Optional[ColumnElement[bool]] = None,
                  amount: int = 0
                  ) -> List[ModelType]:
        statement = self.__build_select(model_class, filter)
        if amount > 0:
            statement = statement.limit(amount)

        result = await self.__session.scalars(statement)
        return list(result.all())

    async def update(self,
                     model_class: ModelType | Type[ModelType],
                     update_data: dict[str, Any],
                     filter: Optional[ColumnElement[bool]] = None,
                     with_commit: bool = False
                     ) -> None:

        statement = update(model_class).values(**update_data)
        if filter is not None:
            statement = statement.where(filter)

        await self.__session.execute(statement)

        if with_commit:
            await self.commit()

    async def delete(self,
                     model_class: ModelType | Type[ModelType],
                     filter: Optional[ColumnElement[bool]] = None,
                     amount: int = 1,
                     with_commit: bool = False
                     ) -> None:

        targets = await self.get(model_class, filter, amount)

        if targets is None:
            return

        for target in targets:
            await self.__session.delete(target)

        if with_commit:
            await self.__session.commit()


    async def commit(self):
        await self.__session.commit()

    async def rollback(self):
        await self.__session.rollback()


