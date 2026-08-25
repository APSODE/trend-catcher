from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.infra.config.setting import get_settings



settings = get_settings()

#보안 없는 api
EXEMPT_PATH_PREFIXES = (
    "/user/local-login",
    "/user/social-login",
    "/user/local-register",
    "/user/social-register",
    "/user/refresh",
    "/health",
    "/docs",
    "/openapi.json",
    "/redoc"
)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if path.startswith(EXEMPT_PATH_PREFIXES):
            return await call_next(request)

        authorization = request.headers.get("Authorization")

        if not authorization:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Unauthorized",
                    "message": "로그인이 필요합니다.",
                }
            )

        return await call_next(request)