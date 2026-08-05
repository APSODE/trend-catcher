from typing import List
from pydantic import BaseModel, ConfigDict
from src.user_api.constant.permission import Permission
from src.user_api.decorator import bind_model
from src.user_api.dto.account_data import AccountData
from src.user_api.dto.hashtag_data import HashtagData
from src.user_api.model import UserModel, UserHashtagModel
from src.user_api.dto.serializer.relation_serializers import _serialize_accounts, _serialize_interest

REQUIRED_RELATIONS = [
    UserModel.accounts,
    (UserModel.interest, UserHashtagModel.hashtag_model),
]

@bind_model(UserModel, relations = REQUIRED_RELATIONS, accounts = _serialize_accounts, interest = _serialize_interest)
class UserData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    name: str
    permission: int | Permission
    accounts: List[AccountData]
    interest: List[HashtagData]
