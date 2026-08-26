from typing import Any, List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.user_api.config import model_config
from src.user_api.model import BaseModel

if TYPE_CHECKING:
    from src.user_api.model import UserHashtagModel

class HashtagModel(BaseModel):
    __tablename__ = "hashtag"
    name: Mapped[str] = mapped_column(String(model_config.HASHTAG_MAX_NAME_LENGTH), unique = True, nullable = False)
    interested_user: Mapped[List["UserHashtagModel"]] = relationship(
        "UserHashtagModel",
        back_populates = "hashtag_model"
    )

    def __init__(self, name: str, **kw: Any):
        super().__init__(**kw)

        self.name = name
