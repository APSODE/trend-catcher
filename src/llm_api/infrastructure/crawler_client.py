from datetime import datetime
import httpx
from src.llm_api.constant.api_constant import CrawlerApiConstant
from src.llm_api.exception.external_exception import CrawlerApiException
from src.llm_api.schema.article import CrawledArticleData
from src.llm_api.infrastructure.base_api_client import BaseApiClient
import logging

logger = logging.getLogger(__name__)

class CrawlerClient(BaseApiClient):
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        super().__init__(
            client = client,
            base_url = base_url,
            exception_class = CrawlerApiException,
            retry_attempts = CrawlerApiConstant.RETRY_ATTEMPTS,
            retry_base_delay = CrawlerApiConstant.RETRY_BASE_DEALY
        )

    #기간 내 기사 조회
    async def get_articles(self, start_date: datetime, end_date: datetime) -> list[CrawledArticleData]:
        params = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat()
        }
        response = await self._get(CrawlerApiConstant.ARTICLES_PATH, CrawlerApiConstant.TIMEOUT, params)
        return [CrawledArticleData.model_validate(item) for item in response]