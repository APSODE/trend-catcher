from typing import List

from pydantic import BaseModel

from src.user_api.constant.permission import Permission
from src.user_api.dto.account_data import AccountData
from src.user_api.dto.user_data import UserData


class RegisterRequest(BaseModel):
    name: str
    permission: int | Permission = Permission.GUEST
    interest: List[int] = []

    login_id: str
    password: str

class LoginRequest(BaseModel):
    login_id: str
    password: str

class DeleteRequest(BaseModel):
    login_id: str
