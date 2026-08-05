from typing import List
from pydantic import BaseModel, ConfigDict
from src.user_api.constant.permission import Permission
from src.user_api.dto.account_data import AccountData


class UserData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    user_account: AccountData
    name: str
    permission: int | Permission
    interest: List[int]

