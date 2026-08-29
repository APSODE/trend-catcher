
import httpx

from src.sns_api.config import get_settings
from src.sns_api.decorator.retry import async_retry
from src.sns_api.model.schema_model import NewsItemData

settings = get_settings()


class CrawlerClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError,),
    )
    # 크롤러 id -> 딕셔너리 형태로 {id: 기사}를 가져옴
    async def get_articles(self, article_ids: list[str]) -> dict[str, NewsItemData]:

        if not article_ids:
            return {}

        response = await self._client.get(
            f"{settings.crawler_api_base_url}/article/articles_ids_sns",
            params={"article_ids": article_ids},
        )
        response.raise_for_status()
        data = response.json()

        result = {}
        for article in data:
            image_url = article["img_list"][0] if article.get("img_list") else None
            item = NewsItemData(
                title=article["title"],
                url=article["url"],
                image_url=image_url,
            )
            result[article["id"]] = item

        return result