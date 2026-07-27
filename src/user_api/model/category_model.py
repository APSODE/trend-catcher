from typing import Optional, TYPE_CHECKING, Any

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.user_api.model.base_model import BaseModel

if TYPE_CHECKING:
    from src.user_api.model.user_category_model import UserCategoryModel

class CategoryModel(BaseModel):
    __tablename__ = "category"
    name: Mapped[str] = mapped_column(String(32), nullable = False)
    description: Mapped[str] = mapped_column(String(255))
    interested_user: Mapped[int] = relationship(
        "UserCategoryModel",
        back_populates = "category_model"
    )

    def __init__(self, name: str, description: str, **kw: Any):
        super().__init__(**kw)

        self.name = name
        self.description = description

