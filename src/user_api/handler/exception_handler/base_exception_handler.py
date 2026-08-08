from typing import Generic, Type, TypeVar

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.user_api.exceptions.app_exception import AppException

E = TypeVar("E", bound = AppException)

#TODO 보일러플레이트로 인한 문제가 발생할 가능성이 높음 -> 추후 Handler 등록과정에 대해 전반적인 개편 예정
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