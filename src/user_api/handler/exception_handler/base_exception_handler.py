from typing import Generic, Type, TypeVar

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.user_api.exceptions.app_exception import AppException

E = TypeVar("E", bound = AppException)


class BaseExceptionHandler(Generic[E]):
    def __init__(self, exception_type: Type[E]):
        self._exception_type = exception_type

    @property
    def exception_type(self) -> Type[E]:
        return self._exception_type

    async def __call__(self, request: Request, exception: Exception) -> JSONResponse:
        status_code = getattr(exception, "status_code", 500)
        return JSONResponse(
            status_code = status_code,
            content = {"detail": str(exception)},
        )