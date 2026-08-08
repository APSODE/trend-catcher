from collections.abc import Iterable
from typing import List, Optional, Type, TypeVar, Any, Sequence, Union

from sqlalchemy import select, update, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, selectinload
from sqlalchemy.orm.interfaces import LoaderOption
from sqlalchemy.sql.elements import ColumnElement

from src.user_api.model.base_model import BaseModel

_RelationPath = Union[InstrumentedAttribute, Sequence[InstrumentedAttribute]]
ModelType = TypeVar("ModelType", bound = BaseModel)

class DatabaseController:
    def __init__(self, session: AsyncSession):
        self.__session = session

    @staticmethod
    def create_object(session: AsyncSession) -> "DatabaseController":
        return DatabaseController(session = session)

    @staticmethod
    def __build_load_option(path: _RelationPath) -> LoaderOption:
        if isinstance(path, InstrumentedAttribute):
            return selectinload(path)

        attributes = list(path)
        option = selectinload(attributes[0])

        for remain_attribute in attributes[1:]:
            option = option.selectinload(remain_attribute)

        return option

    @staticmethod
    def __build_select(model_class: ModelType | Type[ModelType],
                       filter: Optional[ColumnElement[bool]] = None,
                       load_relations: Optional[Sequence[_RelationPath]] = None) -> Select[tuple[Any]]:
        statement = select(model_class)

        if filter is not None:
            statement = statement.where(filter)

        if load_relations:
            for path in load_relations:
                statement = statement.options(DatabaseController.__build_load_option(path))

        return statement

    @property
    def session(self) -> AsyncSession:
        return self.__session

    async def add(self,
                  model: ModelType | Iterable[ModelType],
                  with_flush: bool = False) -> None:
        if isinstance(model, Iterable):
            self.__session.add_all(model)

        else:
            self.__session.add(model)

        if with_flush:
            await self.flush()


    async def get(self,
                  model_class: ModelType | Type[ModelType],
                  filter: Optional[ColumnElement[bool]] = None,
                  load_relations: Optional[Sequence[_RelationPath]] = None,
                  amount: int = 0) -> List[ModelType]:
        statement = self.__build_select(model_class, filter, load_relations)
        if amount > 0:
            statement = statement.limit(amount)

        result = await self.__session.scalars(statement)
        return list(result.all())

    async def update(self,
                     model_class: ModelType | Type[ModelType],
                     update_data: dict[str, Any],
                     filter: Optional[ColumnElement[bool]] = None,
                     with_flush: bool = False) -> None:
        statement = update(model_class).values(**update_data)
        if filter is not None:
            statement = statement.where(filter)

        await self.__session.execute(statement)

        if with_flush:
            await self.flush()

    async def delete(self,
                     model_class: ModelType | Type[ModelType],
                     filter: Optional[ColumnElement[bool]] = None,
                     load_relations: Optional[Sequence[_RelationPath]] = None,
                     amount: int = 1,
                     with_flush: bool = False) -> None:
        targets = await self.get(
            model_class = model_class,
            filter = filter,
            load_relations = load_relations,
            amount = amount
        )

        if targets is None:
            return

        for target in targets:
            await self.__session.delete(target)

        if with_flush:
            await self.__session.flush()


    async def commit(self) -> None:
        await self.__session.commit()

    async def rollback(self) -> None:
        await self.__session.rollback()

    async def flush(self) -> None:
        await self.__session.flush()


