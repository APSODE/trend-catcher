from sqlalchemy import ForeignKey, Float
from src.llm_api.model.base import Base
from sqlalchemy.orm import Mapped, mapped_column

class NewsTopicMapModel(Base):
    __talename__ = "news_topic_map"

    news_id: Mapped[int] = mapped_column(ForeignKey("news_analysis.id"), primary_key = True)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id"), primary_key = True)
    similarity_score: Mapped[float]