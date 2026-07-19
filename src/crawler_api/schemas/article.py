from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict


class ArticleCreate(BaseModel):
    url: str
    title: str
    content: str
    company_name: str
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: datetime | None = None
    crawled_at: datetime
    def __str__(self) -> str:
        return (
            f"[{self.company_name}] {self.title}\n"
            f"  url: {self.url}\n"
            f"  reporter: {self.reporter or '-'}\n"
            f"  category: {self.category or '-'}\n"
            f"  published_at: {self.published_at or '-'}\n"
            f"  crawled_at: {self.crawled_at}\n"
            f"  img_list: {len(self.img_list) if self.img_list else 0}개\n"
            f"  content: {self.content}"
        )
class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    company_name: str | None = None
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: datetime | None = None

class ArticleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    url : str
    id: PydanticObjectId
    title: str
    company_name: str
    crawled_at: datetime
    content: str
    category: str | None = None
    url: str

class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: PydanticObjectId
    url : str
    title: str
    content: str
    company_name: str
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: datetime | None = None
    crawled_at: datetime
    updated_at: datetime | None = None
