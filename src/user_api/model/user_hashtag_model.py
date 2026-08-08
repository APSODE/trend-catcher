from typing import TYPE_CHECKING, Any
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.user_api.model.base_model import BaseModel

if TYPE_CHECKING:
    from src.user_api.model import UserModel, HashtagModel


class UserHashtagModel(BaseModel):
    __tablename__ = "user_hashtag"

    user_fk: Mapped[int] = mapped_column(ForeignKey("user.pk"))
    hashtag_fk: Mapped[int] = mapped_column(ForeignKey("hashtag.pk"))

    user_model: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates = "interest",
    )

    hashtag_model: Mapped["HashtagModel"] = relationship(
        "HashtagModel",
        back_populates = "interested_user"
    )

    def __init__(self, user_fk: int, hashtag_fk: int, **kw: Any):
        super().__init__(**kw)
        self.user_fk = user_fk
        self.hashtag_fk = hashtag_fk



