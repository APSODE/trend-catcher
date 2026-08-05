from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.user_api.auth.jwt_auth import TokenWhitelist
from src.user_api.dto.token_data import TokenType
from src.user_api.exceptions.auth_exceptions import InvalidToken
from src.user_api.utils.jwt_util import JwtUtil

bearer_scheme = HTTPBearer()

async def get_current_account_pk(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> int:
    jwt_token = JwtUtil.decode_token(credentials.credentials, expected_type = TokenType.ACCESS)

    if not await TokenWhitelist.is_registered(jwt_token, credentials.credentials):
        raise InvalidToken()

    return int(jwt_token.account_pk)