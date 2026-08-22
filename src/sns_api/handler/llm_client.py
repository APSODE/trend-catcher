import httpx

from src.sns_api.config import get_settings
from src.sns_api.decorator.retry import async_retry
from src.sns_api.model.schema_model import NewsReferenceData

settings = get_settings()


class LLMClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError,),
    )
    # 주요뉴스
    async def get_major_news(self, limit: int = 10) -> list[NewsReferenceData]:
        # LLM 요청부
        response = await self._client.get(
            f"{settings.llm_api_base_url}/news/daily",
            params={"limit": limit},
        )
        response.raise_for_status()
        data = response.json()

        result = []

        for item in data:
            reference = NewsReferenceData(crawled_id=item["crawled_id"], score=item["score"])
            result.append(reference)

        return result

    # 개인화 뉴스
    async def get_personalized_news(self, user_id: int) -> list[NewsReferenceData]:
        raise NotImplementedError("미정")