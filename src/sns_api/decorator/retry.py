import asyncio
import functools
import logging
import random
from collections.abc import Callable
from typing import Any

logger = logging.getLogger("sns.retry")

def async_retry(
    max_attempts: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 8.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:                                
    if max_attempts < 1:
        raise ValueError("max_attempts는 1 이상")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as exc:
                    if attempt == max_attempts:
                        raise
                    delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
                    delay = min(max_delay, delay + random.uniform(0, delay * 0.25))
                    logger.warning(
                        "%s 실패 (%d/%d): %s — %.2fs 후 재시도",
                        func.__name__, attempt, max_attempts, exc, delay,
                    )
                    await asyncio.sleep(delay)

        return wrapper

    return decorator