from datetime import datetime, timedelta, timezone
from uuid import uuid4

from jwt import (
    encode as encodeJWT,
    decode as decodeJWT,
    InvalidTokenError,
    ExpiredSignatureError
)

from src.user_api.config import auth_config
from src.user_api.dto import JsonWebToken, TokenPair, TokenType, AccountData
from src.user_api.exceptions import InvalidToken, ExpiredToken


class JwtUtil:
    @staticmethod
    def _create_access_token(session_id: str, account: AccountData) -> str:
        return JwtUtil.__create_token(
            session_id = session_id,
            account = account,
            token_type = TokenType.ACCESS,
            expires_delta = timedelta(minutes = auth_config.ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    @staticmethod
    def _create_refresh_token(session_id: str, account: AccountData) -> str:
        return JwtUtil.__create_token(
            session_id = session_id,
            account = account,
            token_type = TokenType.REFRESH,
            expires_delta = timedelta(minutes = auth_config.REFRESH_TOKEN_EXPIRE_MINUTES),
        )

    @staticmethod
    def create_token_pair(session_id: str, account: AccountData) -> TokenPair:
        return TokenPair(
            access_token = JwtUtil._create_access_token(session_id, account),
            refresh_token = JwtUtil._create_refresh_token(session_id, account)
        )

    @staticmethod
    def __create_token(session_id: str, account: AccountData, token_type: TokenType, expires_delta: timedelta) -> str:
        now = datetime.now(timezone.utc)
        token = JsonWebToken(
            jwt_id = str(uuid4()),
            account = account,
            type = token_type,
            iat = now,
            exp = now + expires_delta,
            session_id = session_id
        )
        return encodeJWT(token.model_dump(), auth_config.SECRET_KEY, algorithm = auth_config.ALGORITHM)

    @staticmethod
    def decode_token(token: str, expected_type: TokenType) -> JsonWebToken:
        try:
            payload = decodeJWT(token, auth_config.SECRET_KEY, algorithms = [auth_config.ALGORITHM])
        except ExpiredSignatureError:
            raise ExpiredToken()
        except InvalidTokenError:
            raise InvalidToken()

        if payload.get("type") != expected_type.value:
            raise InvalidToken()

        return JsonWebToken.model_validate(payload)
