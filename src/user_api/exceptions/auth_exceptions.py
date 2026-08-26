from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class InvalidToken(AppException):
    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(self):
        super().__init__(
            "Invalid token data",
            error_code = "AUTH_INVALID_TOKEN",
        )


class ExpiredToken(AppException):
    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(self):
        super().__init__(
            "Current token is expired",
            error_code = "AUTH_TOKEN_EXPIRED",
        )


class MismatchTokenType(AppException):
    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(self):
        super().__init__(
            "Invalid token type",
            error_code = "AUTH_TOKEN_TYPE_MISMATCH",
        )
