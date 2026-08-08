import functools
import logging
from collections.abc import Callable
from typing import Any

from fastapi import HTTPException, status

from src.sns_api.exception.sns_exception import SNSError

logger = logging.getLogger("sns.error")


def handle_errors(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except SNSError as exc:
            raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
        except HTTPException:
            raise
        except Exception as exc:  # noqa: BLE001
            logger.exception("처리되지 않은 오류 in %s", func.__name__)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="internal server error",
            ) from exc

    return wrapper