from abc import ABC, abstractmethod


class BaseUrlFetcher(ABC):

    @abstractmethod
    async def fetch(self, url: str) -> str:
        pass
    @abstractmethod
    async def fetchByAll(self, urls: list[str]) -> list[str]:
        pass