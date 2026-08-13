from pydantic import BaseModel

class AnalysisRunResponseData(BaseModel):
    total: int
    processed: int
    skipped: int
    failed: int

class ScoringRunResponseData(BaseModel):
    scored: int

class NewsResponseData(BaseModel):
    crawled_id: str
    score: float