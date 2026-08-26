from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class UserAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, **kwargs):
        super().__init__(app)
        self.__kwargs = kwargs


    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        pass
