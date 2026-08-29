from src.llm_api.model.base_model import AbstractBaseModel, JsonType
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime
from src.llm_api.util.datetime_util import DateTimeUtil

class TopicModel(AbstractBaseModel):
    __tablename__ = "topic"

    topic: Mapped[str] = mapped_column(String(100)) #주제
    representative_crawled_id: Mapped[str] = mapped_column(String(32))#클러스터 만든 뉴스 id. 디버깅용
    representative_embedding: Mapped[list[float]] = mapped_column(JsonType) #클러스터 만든 뉴스의 임베딩 벡터. 이후 들어오는건 이것과 비교
    count: Mapped[int] = mapped_column(default = 1) #중복도
    first_found_at: Mapped[datetime] = mapped_column(default = DateTimeUtil.get_now_kst, index = True) #클러스터 만들어진 시간