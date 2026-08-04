from pydantic import BaseModel
from datetime import datetime

class CrawledArticleData(BaseModel):
    url: str
    id: str
    title: str
    company_name: str
    crawled_at: datetime
    content: str
    category: str | None = None
