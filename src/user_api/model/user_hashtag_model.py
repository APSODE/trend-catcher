from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.user_api.model.base_model import BaseModel

if TYPE_CHECKING:
    from src.user_api.model.user_model import UserModel
    from src.user_api.model.category_model import CategoryModel


class UserCategoryModel(BaseModel):
    __tablename__ = "user_interest_category"

    user_fk: Mapped[int] = mapped_column(ForeignKey("user.pk"))
    hashtag_fk: Mapped[int] = mapped_column(ForeignKey("hashtag.pk"))

    user_model: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates = "interest",
    )

    category_model: Mapped["CategoryModel"] = relationship(
        "CategoryModel",
        back_populates = "interested_user"
    )


