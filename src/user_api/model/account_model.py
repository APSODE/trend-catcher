from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.user_api.constant.account_constant import MAX_ID_LENGTH, MAX_PW_LENGTH, MAX_SALT_LENGTH
from src.user_api.model.base_model import BaseModel
from src.user_api.model.user_model import UserModel


class AccountModel(BaseModel):
    __tablename__ = "account"
    login_id: Mapped[str] = mapped_column(String(MAX_ID_LENGTH), primary_key = True, unique = True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(MAX_PW_LENGTH), nullable = False)
    personal_salt: Mapped[str] = mapped_column(String(MAX_SALT_LENGTH), nullable = False)

    user: Mapped["UserModel"] = relationship(
        back_populates = "account",
        cascade = "all, delete-orphan"
    )