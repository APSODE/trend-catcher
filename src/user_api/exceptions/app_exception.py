from http import HTTPStatus
from typing import Optional


class AppException(Exception):
    status_code: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR
    error_code: Optional[str] = None

    def __init__(self, message: str, *, status_code: Optional[HTTPStatus] = None, error_code: Optional[str] = None):
        self.message = message

        if status_code is not None:
            self.status_code = status_code

        if error_code is not None:
            self.error_code = error_code

        super().__init__(message)

    def __str__(self) -> str:
        return self.message
