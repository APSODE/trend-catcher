from starlette.requests import Request
from starlette.responses import JSONResponse

from src.user_api.exceptions.auth_exceptions import InvalidToken, ExpiredToken, MismatchTokenType
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler


class InvalidTokenExceptionHandler(BaseExceptionHandler[InvalidToken]):
    def __init__(self):
        super().__init__(InvalidToken)

class ExpiredTokenExceptionHandler(BaseExceptionHandler[ExpiredToken]):
    def __init__(self):
        super().__init__(ExpiredToken)

class MismatchTokenTypeExceptionHandler(BaseExceptionHandler[MismatchTokenType]):
    def __init__(self):
        super().__init__(MismatchTokenType)


