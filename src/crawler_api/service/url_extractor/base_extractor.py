from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    @abstractmethod
    async def parse(
            self,
            raw_content : str,
            selector : str | None = None,
            base_url : str | None = None) -> list[str]:
        pass
