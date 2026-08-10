from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.llm_api.exception.llm_exception import LLMServiceException
import logging

logger = logging.getLogger(__name__)

#llm관련 예외 핸들링
async def handle_llm_service_exception(request: Request, exception: LLMServiceException) -> JSONResponse:
    logger.warning("요청 처리 실패: [%s %s] %s", request.method, request.url.path, exception.message)
    return JSONResponse(status_code = exception.status_code, content = {"detail": exception.message})

#그 외 예외 핸들링
async def handle_unexpected_exception(request: Request, exception: Exception) -> JSONResponse:
    logger.exception("예상 못한 오류: [%s %s]", request.method, request.url.path)
    return JSONResponse(status_code = 500, content = {"detail": "서버 내부 오류 발생"})

#핸들러 등록
def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(LLMServiceException, handle_llm_service_exception) # type: ignore
    app.add_exception_handler(Exception, handle_unexpected_exception)