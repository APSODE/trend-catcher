from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jwt import (
    encode as encodeJWT,
    decode as decodeJWT,
    InvalidTokenError,
    ExpiredSignatureError
)

from src.user_api.constant.auth_constant import (
    SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
)
from src.user_api.exceptions.auth_exceptions import InvalidToken, ExpiredToken

#TODO JWT 인증과정을 Redis를 이용한 별도의 인증과정으로 구현해야함

class JwtUtil:
    @staticmethod
    def create_access_token(account_id: int) -> str:
        return JwtUtil.__create_token(
            account_id = account_id,
            token_type = "access",
            expires_delta = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES),
        )

    @staticmethod
    def create_refresh_token(account_id: int) -> str:
        return JwtUtil.__create_token(
            account_id = account_id,
            token_type = "refresh",
            expires_delta = timedelta(days = REFRESH_TOKEN_EXPIRE_DAYS),
        )

    @staticmethod
    def __create_token(account_id: int, token_type: str, expires_delta: timedelta) -> str:
        now = datetime.now(timezone.utc)
        payload: Dict[str, Any] = {
            "sub": str(account_id),
            "type": token_type,
            "iat": now,
            "exp": now + expires_delta,
        }
        return encodeJWT(payload, SECRET_KEY, algorithm = ALGORITHM)

    @staticmethod
    def decode_token(token: str, expected_type: str) -> int:
        try:
            payload = decodeJWT(token, SECRET_KEY, algorithms = [ALGORITHM])
        except ExpiredSignatureError:
            raise ExpiredToken()
        except InvalidTokenError:
            raise InvalidToken()

        if payload.get("type") != expected_type:
            raise InvalidToken()

        return int(payload.get("sub"))