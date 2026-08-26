from typing import List
from pydantic import BaseModel, ConfigDict
from src.user_api.constant import Permission
from src.user_api.decorator import bind_model, relation
from src.user_api.dto.account_data import LocalAccountData, SocialAccountData
from src.user_api.dto.hashtag_data import HashtagData
from src.user_api.model import UserModel, UserHashtagModel

REQUIRED_RELATIONS = [
    UserModel.local_accounts,
    UserModel.social_accounts,
    (UserModel.interest, UserHashtagModel.hashtag_model),
]

@bind_model(UserModel)
@relation("local_accounts", UserModel.local_accounts, to = LocalAccountData)
@relation("social_accounts", UserModel.social_accounts, to = SocialAccountData)
@relation("interest", UserModel.interest, UserHashtagModel.hashtag_model, to = HashtagData)
class UserData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    name: str
    permission: int | Permission
    local_accounts: List[LocalAccountData]
    social_accounts: List[SocialAccountData]
    interest: List[HashtagData]
