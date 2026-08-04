from typing import Any, TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.user_api.constant.account_constant import MAX_ID_LENGTH, MAX_PW_LENGTH, MAX_SALT_LENGTH
from src.user_api.model.base_model import BaseModel
if TYPE_CHECKING:
    from src.user_api.model.user_model import UserModel


class AccountModel(BaseModel):
    __tablename__ = "account"
    user_fk: Mapped[int] = mapped_column(ForeignKey("user.pk"), nullable = False)
    login_id: Mapped[str] = mapped_column(String(MAX_ID_LENGTH), unique = True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(MAX_PW_LENGTH), nullable = False)
    personal_salt: Mapped[str] = mapped_column(String(MAX_SALT_LENGTH), nullable = False)

    user: Mapped["UserModel"] = relationship(back_populates = "accounts")


    def __init__(self, user_fk: int, login_id: str, hashed_password: str, personal_salt: str, **kw: Any):
        super().__init__(**kw)
        self.user_fk = user_fk
        self.login_id = login_id
        self.hashed_password = hashed_password
        self.personal_salt = personal_salt

    @staticmethod
    def create_model(user_fk: int, login_id: str, hashed_password: str, personal_salt: str):
        return AccountModel(user_fk, login_id, hashed_password, personal_salt)