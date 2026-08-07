from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator

from src.user_api.dto.account_data import AccountData


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class JsonWebToken(BaseModel):
    jwt_id: str
    account: AccountData
    type: TokenType
    iat: datetime
    exp: datetime
    session_id: str


class RefreshJWT(BaseModel):
    access_token_id: str




