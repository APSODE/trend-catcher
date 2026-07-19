from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, JSON
from datetime import datetime

class NewsAnalysisModel(Base):
    __tablename__ = "news_analysis"

    id: Mapped[int] = mapped_column(primary_key = True)
    news_id: Mapped[str] = mapped_column(String(100), index = True) #크롤러에서 받는 id
    category: Mapped[str] = mapped_column(String(10)) #카테고리. 10글자는 안넘어가겠지..?
    topic_id: Mapped[int] = mapped_column(ForeignKey("topic.id")) #주제 id
    score: Mapped[float] #신뢰점수
    score_detail: Mapped[dict | None] = mapped_column(JSON) #디버깅용, 신뢰점수 구하는 과정 저장 #TODO:기능구현 후 Nullable 제거하기
    analyzed_at: Mapped[datetime] = mapped_column(default = datetime.now) #분석한 시간