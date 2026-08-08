from src.llm_api.model.base_model import AbstractBaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

class KeywordModel(AbstractBaseModel):
    __tablename__ = "keyword"

    keyword: Mapped[str] = mapped_column(String(50), unique = True) #키워드
    embedding: Mapped[list[float]] = mapped_column(JSON) #키워드의 임베딩 값. 비교하면서 비슷한거면 병합시킴