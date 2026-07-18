from datetime import datetime
from typing import Annotated

import pymongo
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

    crawled_at : datetime | None = None
    db_updated_at : datetime | None = None # db 데이터 변동

    class Settings:
        name = "article"
        indexes = [
            [("published_at",pymongo.DESCENDING), ("crawled_at", pymongo.ASCENDING)]
        ]
