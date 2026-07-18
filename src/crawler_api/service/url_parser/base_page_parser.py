from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel

class ParsedData(BaseModel):
    title : str
    content : str
    img_urls : list[str] | None = None
    published_at : datetime | None = None
    reporter : str | None = None
    category : str | None = None

class BasePageParser(ABC):

    @abstractmethod
    async def parse(self, content : str) -> ParsedData | None:
        pass