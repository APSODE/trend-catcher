from src.llm_api.model.base import AbstractBaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON

class HashtagModel(AbstractBaseModel):
    __tablename__ = "hashtag"

    hashtag: Mapped[str] = mapped_column(String(32), unique= True) #해시태그 내용
    aliases: Mapped[list[str]] = mapped_column(JSON) #동의어
    children: Mapped[list[str]] = mapped_column(JSON) #하위 개체
    embedding: Mapped[list[float]] = mapped_column(JSON) #임베딩
