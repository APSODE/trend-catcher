from typing import TYPE_CHECKING, Any, Union, List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.user_api.constant.permission import Permission
from src.user_api.constant.user_model_constant import MAX_NAME_LENGTH
from src.user_api.model.base_model import BaseModel
from src.user_api.model.user_category_model import UserCategoryModel

if TYPE_CHECKING:
    from src.user_api.model.account_model import AccountModel


class UserModel(BaseModel):
    __tablename__ = "user"
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), unique = True)
    name: Mapped[str] = mapped_column(String(MAX_NAME_LENGTH), nullable = False)
    permission: Mapped[int] = mapped_column(default = 0, nullable = False)
    interest: Mapped[list["UserCategoryModel"]] = relationship(
        "UserCategoryModel",
        back_populates = "user_model",
    )

    accounts: Mapped[List["AccountModel"]] = relationship(
        back_populates = "user",
        cascade = "all, delete-orphan"
    )



    def __init__(self, name: str, permission: Union[int, Permission], interest: Optional[List[int]] = None, **kw: Any):
        super().__init__(**kw)
        self.name = name

        if isinstance(permission, Permission):
            self.permission = permission.value
        else:
            self.permission = permission

        if interest is None:
            self.interest = []

    @staticmethod
    def create_model(name: str, permission: Union[int, Permission], interest: Optional[List[int]] = None):
        return UserModel(name, permission, interest)





