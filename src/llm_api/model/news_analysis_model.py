from src.llm_api.model.base_model import AbstractBaseModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, JSON, Float
from datetime import datetime
from src.llm_api.util.datetime_util import DateTimeUtil

class NewsAnalysisModel(AbstractBaseModel):
    __tablename__ = "news_analysis"

    crawled_id: Mapped[str] = mapped_column(String(32), unique=True, index = True) #크롤러에서 받는 id
    category: Mapped[str | None] = mapped_column(String(50)) #카테고리
    topic_fk: Mapped[int] = mapped_column(ForeignKey("topic.pk")) #주제 pk
    score: Mapped[float | None] = mapped_column(Float) #최종 신뢰점수
    content_score: Mapped[float] = mapped_column(Float)  # LLM 자체 평가 (분석 시점)
    cross_check_score: Mapped[float | None] = mapped_column(Float)  # 중복도 (산정 시점)
    analyzed_at: Mapped[datetime] = mapped_column(default = DateTimeUtil.get_now_kst) #분석한 시간