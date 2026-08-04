from sqlalchemy import ForeignKey, UniqueConstraint
from src.llm_api.model.base import AbstractBaseModel
from sqlalchemy.orm import Mapped, mapped_column

class NewsKeywordMapModel(AbstractBaseModel):
    __tablename__ = "news_keyword_map"
    __table_args__ = (UniqueConstraint("news_fk", "keyword_fk"),)

    news_fk: Mapped[int] = mapped_column(ForeignKey("news_analysis.pk"))
    keyword_fk: Mapped[int] = mapped_column(ForeignKey("keyword.pk"))