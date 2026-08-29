from pydantic import BaseModel, ConfigDict

from src.user_api.constant import AccountProvider, AccountType
from src.user_api.decorator import bind_model
from src.user_api.model import LocalAccountModel, SocialAccountModel

@bind_model(LocalAccountModel, SocialAccountModel)
class AccountData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    user_fk: int
    account_type: AccountType

@bind_model(LocalAccountModel)
class LocalAccountData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    user_fk: int
    login_id: str

@bind_model(SocialAccountModel)
class SocialAccountData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    user_fk: int
    provider: AccountProvider
    provider_user_id: str
