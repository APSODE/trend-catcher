from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict


class ArticleBase(BaseModel):
    url : str
    title : str
    content : str
    company_name : str
    reporter : str | None = None
    category : str | None = None
    img_list : list[str] | None = None
    published_at : str | None = None

class ArticleCreate(ArticleBase):
    pass

class ArticleUpdate(ArticleBase):
    title: str | None = None
    content: str | None = None
    company_name: str | None = None
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: str | None = None

class ArticleRead(ArticleBase):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: PydanticObjectId
    title: str
    company_name: str
    crawled_at: datetime
    content: str
    category: str | None = None
    url: str