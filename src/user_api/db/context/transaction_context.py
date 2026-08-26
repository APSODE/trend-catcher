from typing import Callable, Dict, Type, TypeVar, AsyncGenerator

from src.user_api.db import DatabaseController, DatabaseCreator
from src.user_api.repository import (
    BaseRepository,
    HashtagRepository,
    LocalAccountRepository,
    SocialAccountRepository,
    UserHashtagRepository,
    UserRepository,
)

R = TypeVar("R", bound = BaseRepository)


class TransactionContext:
    def __init__(
        self,
        session_factory,
        repository_factories: Dict[Type[BaseRepository], Callable[[DatabaseController], BaseRepository]],
    ):
        self._session_factory = session_factory
        self._repository_factories = repository_factories
        self._instances: Dict[Type[BaseRepository], BaseRepository] = {}

    async def __aenter__(self) -> "TransactionContext":
        self._session = self._session_factory()
        self._controller = DatabaseController(self._session)
        return self

    def get_repository(self, repository_type: Type[R]) -> R:
        if repository_type not in self._instances:
            factory = self._repository_factories[repository_type]
            self._instances[repository_type] = factory(self._controller)
        return self._instances[repository_type]

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type is None:
                await self._controller.commit()
            else:
                await self._controller.rollback()
        finally:
            await self._session.close()


_REPOSITORY_FACTORIES: Dict[Type[BaseRepository], Callable] = {
    UserRepository: UserRepository,
    LocalAccountRepository: LocalAccountRepository,
    SocialAccountRepository: SocialAccountRepository,
    HashtagRepository: HashtagRepository,
    UserHashtagRepository: UserHashtagRepository,
}


async def _get_transaction_context() -> AsyncGenerator[TransactionContext, None]:
    context = TransactionContext(
        session_factory = DatabaseCreator().session,
        repository_factories = _REPOSITORY_FACTORIES,
    )
    async with context:
        yield context
