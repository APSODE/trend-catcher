from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.user_api.model.base_model import BaseModel

if TYPE_CHECKING:
    from src.user_api.model.user_model import UserModel


class UserCategoryModel(BaseModel):
    __tablename__ = "user_interest_category"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key = True)
    category_id: Mapped[int] = mapped_column(primary_key = True)

    user_model: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="interest",
    )


