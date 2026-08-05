from typing import Generic, TypeVar, Type
from src.llm_api.model.base_model import AbstractBaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy import Select, select

ModelType = TypeVar("ModelType", bound = AbstractBaseModel) #타입체크 방지턱

class AbstractBaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model_class: Type[ModelType]):
        self._session = session
        self._model_class = model_class

    #저장
    async def save(self, model: ModelType) -> ModelType:
        self._session.add(model)
        await self._session.flush()
        return model

    #여럿 저장
    async def save_all(self, models: list[ModelType]) -> list[ModelType]:
        if not models: #빈 모델이 들어오면 터지는거 방지
            return models

        self._session.add_all(models)
        await self._session.flush()
        return models

    #외래키로 탐색
    async def get_by_pk(self, pk: int) -> ModelType | None:
        return await self._session.get(self._model_class, pk)

    #셀렉트문 헬퍼
    def _select(self, condition: ColumnElement[bool] | None = None) -> Select[tuple[ModelType]]:
        stmt = select(self._model_class)
        if condition is not None:
            stmt = stmt.where(condition)
        return stmt

    #검색 헬퍼: 단일 대상
    async def _find_one(self, condition: ColumnElement[bool] | None = None) -> ModelType | None:
        return await self._session.scalar(self._select(condition))

    #검색 헬퍼: 여러 대상
    async def _find_all(self, condition: ColumnElement[bool] | None = None) -> list[ModelType]: #list는 검색결과 없어도 빈 리스트 리턴
        result = await self._session.scalars(self._select(condition))
        return list(result.all())