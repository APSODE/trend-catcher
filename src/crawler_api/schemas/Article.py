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

class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    company_name: str | None = None
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: datetime | None = None

class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: PydanticObjectId
    title: str
    company_name: str
    crawled_at: datetime
    content: str
    category: str | None = None
    url: str