from abc import ABC, abstractmethod


class BaseUrlFetcher(ABC):

    @abstractmethod
    async def fetch(self, url: str) -> str:
        pass
    @abstractmethod
    async def fetch_by_all(self, urls: list[str], base_url : str) -> list[str]:
        pass