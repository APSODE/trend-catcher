from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class JsonWebToken(BaseModel):
    jwt_id: str
    account_pk: int
    type: TokenType
    iat: datetime
    exp: datetime
    session_id: str

    @field_validator("account_pk", mode = "before")
    @classmethod
    def parse_account_pk(cls, value):
        return int(value)

class RefreshJWT(BaseModel):
    access_token_id: str




