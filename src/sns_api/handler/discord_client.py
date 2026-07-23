import httpx

from src.sns_api.config import get_settings
from src.sns_api.decorator.retry import async_retry
from src.sns_api.model.schema_model import NewsBundleData, NewsItemData
import logging

settings = get_settings()
logger = logging.getLogger("sns.discord")


class TransientWebhookError(Exception):
    """일시적 실패 — 재시도 대상."""


class PermanentWebhookError(Exception):
    """영구적 실패 — 재시도하지 않음."""


def build_payload(bundle: NewsBundleData, slot_label: str) -> dict:
    fields = []
    if bundle.major:
        lines = [f"{i}. {item.title}" for i, item in enumerate(bundle.major, start=1)]
        fields.append({"name": "📰 주요 뉴스", "value": "\n".join(lines)})
    if bundle.personalized:
        lines = [f"{i}. {item.title}" for i, item in enumerate(bundle.personalized, start=1)]
        fields.append({"name": "✨ 맞춤 뉴스", "value": "\n".join(lines)})

    return {
        "username": "Trend Catcher",
        "embeds": [{"title": f"{slot_label} 뉴스 브리핑", "fields": fields}],
    }


class DiscordClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError, TransientWebhookError),
    )
    async def send(self, webhook_url: str, payload: dict) -> None:
        resp = await self._client.post(webhook_url, json=payload)

        if resp.status_code in (200, 204):
            return

        if resp.status_code == 429:
            raise TransientWebhookError("rate limited (429)")

        if 400 <= resp.status_code < 500:
            raise PermanentWebhookError(f"permanent error {resp.status_code}")

        raise TransientWebhookError(f"server error {resp.status_code}")
