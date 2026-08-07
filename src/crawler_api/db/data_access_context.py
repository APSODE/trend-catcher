from typing import Callable, Dict, Type, TypeVar

from pymongo.asynchronous.client_session import AsyncClientSession

from src.crawler_api.repository.base_repository import BaseRepository

Repository = TypeVar("Repository", bound=BaseRepository)


class DataAccessContext:

    def __init__(self, client, repository_factories: dict[Type[Repository], Callable[[AsyncClientSession | None], Repository]], transaction: bool = False) -> None:

        self._repository_factories = repository_factories
        self._instances: Dict[Type[Repository], Repository] = {}
        self._client = client
        self._transaction = transaction
        self._session: AsyncClientSession | None = None

    def get_repository(self, repository_type: Type[Repository]) -> Repository:
        if repository_type not in self._instances:
            factory = self._repository_factories[repository_type]
            self._instances[repository_type] = factory(self._session)
        return self._instances[repository_type]



    async def __aenter__(self) -> "DataAccessContext":
        if self._transaction:
            session = self._client.start_session()

            try:
                await session.start_transaction()
            except Exception:
                await session.end_session()
                raise
            
            self._session = session
        return self

    async def __aexit__(self, exc_type, exc, tb):

        if self._session is None:
            return

        try:
            if self._transaction:
                if exc_type:
                    await self._session.abort_transaction()
                else:
                    await self._session.commit_transaction()
        finally:
            await self._session.end_session()

    @property
    def session(self) -> AsyncClientSession | None:
        return self._session