import httpx

from src.crawler_api.event.event_publisher import EventObserver
from src.crawler_api.event.event_types import DomainEvent, EventType
from src.crawler_api.schemas.article import ArticleResponseSNS


class SNSApiObserver(EventObserver):
    def __init__(self, url: str):
        self._url = url

    async def on_event(self, event: DomainEvent):
        if event.event_type != EventType.CREATED:
            return
        articles = event.payload.get("articles", [])
        sns_payload = [
            ArticleResponseSNS.model_validate(article).model_dump(mode="json") for article in articles
        ]

        async with httpx.AsyncClient() as client:
            response = await client.post(self._url, json={"articles": sns_payload})
            response.raise_for_status()
