import logging
from http import HTTPStatus

from starlette.requests import Request
from starlette.responses import JSONResponse

from src.user_api.exceptions import AppException

logger = logging.getLogger("user_api.exception")


class AppExceptionHandler:
    async def __call__(self, request: Request, exception: AppException) -> JSONResponse:
        status_code = getattr(exception, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR)
        status_code_value = getattr(status_code, "value", status_code)

        if status_code_value >= 500:
            logger.exception(
                "Unhandled AppException on %s %s: %s",
                request.method, request.url.path, exception.message,
                exc_info = exception,
            )
        else:
            logger.warning(
                "%s on %s %s: %s",
                type(exception).__name__, request.method, request.url.path, exception.message,
            )

        content = {"detail": exception.message}
        if exception.error_code is not None:
            content["error_code"] = exception.error_code

        return JSONResponse(
            status_code = status_code_value,
            content = content,
        )


class UnhandledExceptionHandler:
    async def __call__(self, request: Request, exception: Exception) -> JSONResponse:
        logger.exception(
            "Unexpected exception on %s %s",
            request.method, request.url.path,
            exc_info = exception,
        )

        return JSONResponse(
            status_code = HTTPStatus.INTERNAL_SERVER_ERROR,
            content = {"detail": "Internal server error"},
        )


def register_exception_handlers(app) -> None:
    app.add_exception_handler(AppException, AppExceptionHandler())
    app.add_exception_handler(Exception, UnhandledExceptionHandler())
