from sqlalchemy import ForeignKey

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class NewsKeywordMapModel(Base):
    __tablename__ = "news_keyword_map"

    news_id: Mapped[int] = mapped_column(ForeignKey("news_analysis.id"), primary_key = True)
    keyword_id: Mapped[int] = mapped_column(ForeignKey("keyword.id"), primary_key = True)