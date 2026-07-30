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
    image_url = None  # embed 하나에 이미지는 1개만 가능, 첫 번째로 발견되는 것 사용

    def format_lines(items):
        nonlocal image_url
        lines = []
        for i, item in enumerate(items, start=1):
            if item.url:
                lines.append(f"{i}. [{item.title}]({item.url})")
            else:
                lines.append(f"{i}. {item.title}")
            if image_url is None and item.image_url:
                image_url = item.image_url
        return lines

    if bundle.major:
        fields.append({"name": "📰 주요 뉴스", "value": "\n".join(format_lines(bundle.major))})
    if bundle.personalized:
        fields.append({"name": "✨ 맞춤 뉴스", "value": "\n".join(format_lines(bundle.personalized))})

    embed = {"title": f"{slot_label} 뉴스 브리핑", "fields": fields}
    if image_url:
        embed["image"] = {"url": image_url}

    return {"username": "Trend Catcher", "embeds": [embed]}


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
