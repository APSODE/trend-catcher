from typing import Type, TypeVar, Awaitable, Callable

from fastapi import Depends

from src.user_api.db.context import get_transaction_context, TransactionContext
from src.user_api.repository import BaseRepository

T = TypeVar("T", bound = "BaseService")


class BaseService:
    @classmethod
    def create_dependency(cls: Type[T], **repository_types: Type[BaseRepository]) -> Callable[..., Awaitable[T]]:
        async def _get_service(context: TransactionContext = Depends(get_transaction_context)) -> T:
            kwargs = {
                param_name: context.get_repository(repo_type)
                for param_name, repo_type in repository_types.items()
            }
            return cls(**kwargs)

        return _get_service
