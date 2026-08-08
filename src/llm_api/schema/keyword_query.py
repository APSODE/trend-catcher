from pydantic import BaseModel

class KeywordQueryData(BaseModel):
    terms: list[str]
    embedding: list[float]