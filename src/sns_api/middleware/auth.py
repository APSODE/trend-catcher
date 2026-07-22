from fastapi import Header, HTTPException, status
from src.sns_api.config import get_settings

settings = get_settings()  # ← 이 줄 추가!


class InternalTokenMiddleware:
    async def __call__(
            self, x_internal_token: str | None = Header(default=None)
    ) -> None:
        if x_internal_token != settings.internal_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid internal token",
            )
