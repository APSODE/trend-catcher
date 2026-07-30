from abc import ABC
from typing import Generic, Type, TypeVar

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.user_api.exceptions.app_exception import AppException

E = TypeVar("E", bound = AppException)


class BaseExceptionHandler:
    def __init__(self, status_code: int = AppException.status_code):
        self._status_code = status_code

    @property
    def get_status_code(self) -> int:
        return self._status_code

    async def __call__(self, request: Request, exception: Exception) -> JSONResponse:
        status_code = getattr(exception, "status_code", 500)
        return JSONResponse(
            status_code = status_code,
            content = {"detail": str(exception)},
        )
