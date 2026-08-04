from typing import Any, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.user_api.model.base_model import BaseModel
from src.user_api.model.user_hashtag_model import UserHashtagModel

class HashtagModel(BaseModel):
    __tablename__ = "hashtag"
    name: Mapped[str] = mapped_column(String(32), unique = True, nullable = False)
    interested_user: Mapped[List["UserHashtagModel"]] = relationship(
        "UserHashtagModel",
        back_populates = "hashtag_model"
    )

    def __init__(self, name: str, **kw: Any):
        super().__init__(**kw)

        self.name = name

