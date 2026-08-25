from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from src.llm_api.model.base_model import AbstractBaseModel, JsonType
from src.llm_api.util.datetime_util import DateTimeUtil

class SearchCacheModel(AbstractBaseModel):
    __tablename__ = "search_cache"

    result: Mapped[dict] = mapped_column(JsonType)
    searched_at: Mapped[datetime] = mapped_column(default = DateTimeUtil.get_now_kst, index = True)
    