from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

class KeywordModel(Base):
    __tablename__ = "keyword"
    id: Mapped[int] = mapped_column(primary_key = True)
    keyword_text: Mapped[str] = mapped_column(String(50), unique = True) #키워드
    embedding: Mapped[list] = mapped_column(JSON) #키워드의 임베딩 값. 비교하면서 비슷한거면 병합시킴