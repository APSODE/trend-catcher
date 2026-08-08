import pymongo

from datetime import datetime
from typing import Annotated
from beanie import Document, Indexed


class Article(Document):
    # 중복 방지용
    url : Annotated[str, Indexed(unique=True)]

    title: str
    content: str
    company_name: str
    reporter: str | None = None
    category: str | None = None
    img_list: list[str] | None = None
    published_at: datetime | None = None

    crawled_at: datetime
    db_updated_at: datetime | None = None # db 데이터 변동

    class Settings:
        name = "article"
        # 인덱스 생성
        indexes = [[("published_at",pymongo.ASCENDING), ("crawled_at", pymongo.DESCENDING)]]
