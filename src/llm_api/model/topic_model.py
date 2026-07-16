from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, JSON
from datetime import datetime

class TopicModel(Base):
    __tablename__ = "topic"

    id: Mapped[int] = mapped_column(primary_key=True)
    topic_name: Mapped[str] = mapped_column(String(100)) #주제. 100자가 넘어가면 그건 주제가 문제이지 않을까, 100자넘으면 다시써오라고 턴백시키는 안전장치 필요할듯
    representative_news_id: Mapped[str] = mapped_column(String(100))#클러스터 만든 뉴스 id. 디버깅용
    representative_embedding: Mapped[list] = mapped_column(JSON) #클러스터 만든 뉴스의 임베딩 벡터. 이후 들어오는건 이것과 비교
    count: Mapped[int] = mapped_column(default = 1) #중복도
    first_seen_at: Mapped[datetime] = mapped_column(default = datetime.now) #클러스터 만들어진 시간

