from datetime import timezone, datetime
from typing import Annotated

import pymongo
from pydantic import Field
from beanie import Document, Indexed


class Article(Document):
    # 중복 방지용
    url : Annotated[str, Indexed(unique=True)]

    title : str
    content : str
    company_name : str
    reporter : str | None = None
    category : str | None = None
    img_list : list[str] | None = None
    published_at : datetime | None = None
    crawled_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at : datetime | None = None

    class Settings:
        name = "article"
        indexes = [
            [("published_at",pymongo.DESCENDING), ("crawled_at", pymongo.ASCENDING)]
        ]
