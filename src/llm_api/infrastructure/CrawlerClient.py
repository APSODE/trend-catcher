import asyncio
from datetime import datetime
import httpx
from src.llm_api.constant.crawler_constant import CrawlerConstant
from src.llm_api.exception.llm_exception import CrawlerApiException
from src.llm_api.schema.article import CrawledArticleData

import logging

logger = logging.getLogger(__name__)

class CrawlerClient:
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        self._client = client
        self._base_url = base_url.rstrip("/")

    #기간 내 기사 조회
    async def get_articles(self, start_date: datetime, end_date: datetime) -> list[CrawledArticleData]:
        url = f"{self._base_url}{CrawlerConstant.ARTICLES_PATH}"
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }

        for attempt in range(CrawlerConstant.RETRY_ATTEMPTS):
            try:
                response = await self._client.get(url, params = params, timeout = CrawlerConstant.TIMEOUT)
                response.raise_for_status()
                return [CrawledArticleData.model_validate(item) for item in response.json()]
            except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError) as error:
                if attempt == CrawlerConstant.RETRY_ATTEMPTS - 1:
                    raise CrawlerApiException("크롤러 api 호출 실패") from error
                delay = CrawlerConstant.RETRY_BASE_DEALY * (2 ** attempt)
                logger.warning("크롤러 호출 실패, 재시도 (%d회차, %.1f초 후", attempt + 1, delay)
                await asyncio.sleep(delay)
        raise RuntimeError("크롤러 재시도 횟수 설정 잘못됨")