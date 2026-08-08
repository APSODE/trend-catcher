from datetime import datetime
from beanie import PydanticObjectId
from pydantic import BaseModel, ConfigDict, field_serializer


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

class ArticleUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    company_name: str | None = None
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: datetime | None = None

class ArticleResponseLLM(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: PydanticObjectId
    title: str
    content: str

    @field_serializer("id")
    def serialize_object_id(self, value):
        return str(value)

class ArticleResponseSNS(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    url: str
    id: PydanticObjectId
    title: str
    company_name: str
    published_at: datetime
    img_list: list[str] | None = None

    @field_serializer("id")
    def serialize_object_id(self, value):
        return str(value)


class ArticleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: PydanticObjectId
    url: str
    title: str
    content: str
    company_name: str
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: datetime | None = None
    crawled_at: datetime
    db_updated_at: datetime | None = None

    @field_serializer("id")
    def serialize_object_id(self, value):
        return str(value)
