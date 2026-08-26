from typing import Optional

import httpx
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.infra.config.setting import get_settings



settings = get_settings()

class _BearerAuth(httpx.Auth):
    def __init__(self, token: str):
        self.token = token

    def auth_flow(self, request):
        request.headers['Authorization'] = f'{self.token}'
        yield request

async def _is_valid_token(request: Request) -> bool:
    jwt = request.headers.get("authorization")
    if jwt is None:
        return False

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url = settings.jwt_check_url,
            auth = _BearerAuth(jwt)
        )

        return response.status_code == 200

def _is_unprotected_url(request: Request) -> bool:
    return request.url.path.startswith(settings.unprotected_url)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        is_protected_url = not _is_unprotected_url(request)
        is_invalid_token = not await _is_valid_token(request)

        if is_protected_url and is_invalid_token:
            return JSONResponse(
                status_code = 401,
                content = {
                    "detail": "Unauthorized",
                    "message": "로그인이 필요합니다.",
                }
            )

        return await call_next(request)
