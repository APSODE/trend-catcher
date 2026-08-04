from pydantic import BaseModel, Field
from datetime import datetime

class CrawledArticleData(BaseModel):
    url: str
    crawled_id: str = Field(alias="id")
    title: str
    company_name: str
    crawled_at: datetime
    content: str
    category: str | None = None
