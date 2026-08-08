from typing import Any, TYPE_CHECKING

from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.user_api.constant.account_constant import (
    MAX_ID_LENGTH, MAX_PW_LENGTH, MAX_SALT_LENGTH,
    AccountProvider, AccountType, LOCAL, SOCIAL
)
from src.user_api.model.base_model import BaseModel
if TYPE_CHECKING:
    from src.user_api.model import UserModel


class LocalAccountModel(BaseModel):
    __tablename__ = "local_account"
    user_fk: Mapped[int] = mapped_column(ForeignKey("user.pk"), nullable = False)
    account_type: Mapped[AccountType] = mapped_column(default = LOCAL, nullable = False)
    login_id: Mapped[str] = mapped_column(String(MAX_ID_LENGTH), unique = True, nullable = False)
    hashed_password: Mapped[str] = mapped_column(String(MAX_PW_LENGTH), nullable = False)
    personal_salt: Mapped[str] = mapped_column(String(MAX_SALT_LENGTH), nullable = False)

    user: Mapped["UserModel"] = relationship(back_populates = "local_accounts")


    def __init__(self, user_fk: int, login_id: str, hashed_password: str, personal_salt: str, **kw: Any):
        super().__init__(**kw)
        self.user_fk = user_fk
        self.login_id = login_id
        self.hashed_password = hashed_password
        self.personal_salt = personal_salt

    @staticmethod
    def create_model(user_fk: int, login_id: str, hashed_password: str, personal_salt: str) -> "LocalAccountModel":
        return LocalAccountModel(user_fk, login_id, hashed_password, personal_salt)

class SocialAccountModel(BaseModel):
    __tablename__ = "social_account"
    __table_args__ = (
        UniqueConstraint(
            "provider", "provider_user_id",
            name = "uq_provider_account"
        ),
    )

    user_fk: Mapped[int] = mapped_column(ForeignKey("user.pk"), nullable = False)
    account_type: Mapped[AccountType] = mapped_column(default = SOCIAL, nullable = False)
    provider_user_id: Mapped[str] = mapped_column(String(MAX_ID_LENGTH), nullable = False)
    provider: Mapped[AccountProvider] = mapped_column(nullable = False)

    user: Mapped["UserModel"] = relationship(back_populates = "social_accounts")

    def __init__(self, user_fk: int, provider: AccountProvider, provider_user_id: str, **kw: Any):
        super().__init__(**kw)
        self.user_fk = user_fk
        self.provider = provider
        self.provider_user_id = provider_user_id

    @staticmethod
    def create_model(user_fk: int, provider: AccountProvider, provider_user_id: str) -> "SocialAccountModel":
        return SocialAccountModel(user_fk, provider, provider_user_id)