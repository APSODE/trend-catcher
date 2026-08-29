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
    # 주요뉴스 (크롤러 아이디가 담긴 리스트를 가져옴)
    async def get_major_news(self, limit: int = 10) -> list[NewsReferenceData]:
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

    # 유저의 해시태그로 매칭된 기사 크롤러 아이디 목록 조회
    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError,),
    )
    async def search_hashtags(self, hashtags: list[str]) -> dict[str, list[str]]:
        if not hashtags:
            return {}
        response = await self._client.post(
            f"{settings.llm_api_base_url}/hashtag/search",
            json={"hashtags": hashtags},
        )
        response.raise_for_status()
        return response.json()