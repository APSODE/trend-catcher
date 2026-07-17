from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.user_api.model.base_model import BaseModel

if TYPE_CHECKING:
    from src.user_api.model.user_category_model import UserCategoryModel


class UserModel(BaseModel):
    __tablename__ = "user"

    login_id: Mapped[str] = mapped_column(String(32), unique = True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable = False)

    name: Mapped[str] = mapped_column(String(16), nullable=False)
    permission: Mapped[int] = mapped_column(default=0)
    interest: Mapped[list["UserCategoryModel"]] = relationship(
        "UserCategoryModel",
        back_populates = "user_model",
    )





