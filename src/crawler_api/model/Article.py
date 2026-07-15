from datetime import timezone, datetime

import pymongo
from pydantic import Field
from beanie import Document, Indexed


class article(Document):
    # 중복 방지용
    url : Indexed(str, unique=True)

    title : str
    content : str
    company_name : str
    reporter : str | None = None
    category : str | None = None
    img_list : list[str] | None = None
    published_at : datetime | None = None
    crawled_at : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "article"
        indexes = [
            [("published_at",pymongo.DESCENDING)]
        ]
