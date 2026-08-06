from typing import List
from pydantic import BaseModel, ConfigDict
from src.user_api.constant.permission import Permission
from src.user_api.decorator import bind_model, relation
from src.user_api.dto.account_data import AccountData
from src.user_api.dto.hashtag_data import HashtagData
from src.user_api.model import UserModel, UserHashtagModel

REQUIRED_RELATIONS = [
    UserModel.accounts,
    (UserModel.interest, UserHashtagModel.hashtag_model),
]

@bind_model(UserModel)
@relation("accounts", UserModel.accounts, to = AccountData)
@relation("interest", UserModel.interest, UserHashtagModel.hashtag_model, to = HashtagData)
class UserData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    name: str
    permission: int | Permission
    accounts: List[AccountData]
    interest: List[HashtagData]
