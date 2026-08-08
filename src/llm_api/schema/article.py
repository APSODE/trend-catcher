from pydantic import BaseModel, Field
from datetime import datetime

class CrawledArticleData(BaseModel):
    # url: str
    crawled_id: str = Field(alias="id") # dd
    title: str # dd
    # company_name: str
    # crawled_at: datetime
    content: str # dd
    # category: str | None = None
