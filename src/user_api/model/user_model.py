from typing import TYPE_CHECKING, Any, Union, List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.user_api.constant.permission import Permission
from src.user_api.constant.user_model_constant import MAX_ID_LENGTH, MAX_PW_LENGTH, MAX_NAME_LENGTH
from src.user_api.model.base_model import BaseModel

if TYPE_CHECKING:
    from src.user_api.model.user_category_model import UserCategoryModel


class UserModel(BaseModel):
    __tablename__ = "user"

    login_id: Mapped[str] = mapped_column(String(MAX_ID_LENGTH), unique = True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(MAX_PW_LENGTH), nullable = False)

    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable = False)
    permission: Mapped[int] = mapped_column(default = 0, nullable = False)
    interest: Mapped[list["UserCategoryModel"]] = relationship(
        "UserCategoryModel",
        back_populates = "user_model",
    )

    def __init__(self, login_id: str, password: str, name: str, permission: Union[int, Permission], interest: Optional[List[int]] = None, **kw: Any):
        super().__init__(**kw)
        self.login_id = login_id
        self.hashed_password = password
        self.name = name

        if isinstance(permission, Permission):
            self.permission = permission.value
        else:
            self.permission = permission

        if interest is None:
            self.interest = []

    @staticmethod
    def create_model(login_id: str, password: str, name: str, permission: Union[int, Permission], interest: Optional[List[int]] = None):
        return UserModel(login_id, password, name, permission, interest)





