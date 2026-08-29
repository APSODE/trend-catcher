import asyncio
import httpx
from typing import Any, Type
from src.llm_api.exception.external_exception import ExternalApiException
import logging

logger = logging.getLogger(__name__)

class BaseApiClient:
    def __init__(self, client:httpx.AsyncClient, base_url: str, exception_class: Type[ExternalApiException], retry_attempts: int, retry_base_delay: float, default_headers: dict[str, str] | None = None):
        self._client = client
        self._base_url = base_url.rstrip("/")
        self._exception_class = exception_class
        self._retry_attempts = retry_attempts
        self._retry_base_delay = retry_base_delay
        self._default_headers = default_headers

    async def _get(self, path: str, timeout: float, params: dict | None = None) -> Any:
        return await self._request_with_retry("GET", path, timeout, params = params)

    async def _post(self, path: str, timeout: float, payload: dict) -> Any:
        return await self._request_with_retry("POST", path, timeout, json = payload)

    async def _request_with_retry(self, method: str, path: str, timeout: float, **kwargs: Any) -> Any:
        url = f"{self._base_url}{path}"

        for attempt in range(self._retry_attempts):
            try:
                response = await self._client.request(method, url, timeout = timeout, headers = self._default_headers, **kwargs)
                response.raise_for_status()
                return response.json()
            except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError) as error:
                if attempt == self._retry_attempts - 1:
                    raise self._exception_class(f"API 호출 실패: {method} {url}") from error
                delay = self._retry_base_delay * (2 ** attempt)
                logger.warning("API 호출 실패, 재시도: [%s, %d회차, %.1f초 후]", url, attempt + 1, delay)
                await asyncio.sleep(delay)
        raise RuntimeError("재시도 횟수 설정 잘못됨")
