from typing import List, Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict

from src.user_api.constant.account_constant import AccountProvider
from src.user_api.decorator import bind_model, relation
from src.user_api.dto import HashtagData, AccountData
from src.user_api.model import UserModel, SocialAccountModel, UserHashtagModel

_DTO = TypeVar("_DTO", bound = BaseModel)

class DataCollectionResponse(BaseModel, Generic[_DTO]):
    amount: int
    datas: List[_DTO]

@bind_model(SocialAccountModel)
class PKResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int

@bind_model(UserModel)
@relation("local_accounts", UserModel.local_accounts, to = AccountData)
@relation("social_accounts", UserModel.social_accounts, to = AccountData)
@relation("interest", UserModel.interest, UserHashtagModel.hashtag_model, to = HashtagData)
class UserSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    name: str
    local_accounts: List[AccountData]
    social_accounts: List[AccountData]
    interest: List[HashtagData]

class OAuth2Response(BaseModel):
    name: Optional[str] = None
    provider: AccountProvider
    provider_user_id: str
