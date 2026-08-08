import httpx

from src.sns_api.config import get_settings
from src.sns_api.decorator.retry import async_retry
from src.sns_api.model.schema_model import NewsBundleData

settings = get_settings()

DISCORD_API_BASE = "https://discord.com/api/v10"


class TransientWebhookError(Exception):
    """일시적 실패 - 재시도 대상"""


class PermanentWebhookError(Exception):
    """영구적 실패 - 재시도하지 않음"""


# 디스코드 디엠 메세지 내용
def build_payload(bundle: NewsBundleData, slot_label: str) -> dict:
    field = []
    # 주요 뉴스 내용상자
    if bundle.major:
        lines = []
        for i, item in enumerate(bundle.major, start=1):
            line = f"{i}. {item.title}"
            lines.append(line)
        field.append({"name": "주요 뉴스", "value": "\n".join(lines)})

    # 개인화된 뉴스 내용상자
    if bundle.personalized:
        lines = []
        for i, item in enumerate(bundle.personalized, start=1):
            line = f"{i}. {item.title}"
            lines.append(line)
        field.append({"name": "개인화된 뉴스", "value": "\n".join(lines)})

    return {
        "username": "Trend Catcher",
        "embeds": [{"title": f"{slot_label} 뉴스 브리핑", "fields": field}],
    }


class DiscordClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    def _headers(self) -> dict:
        return {"Authorization": f"Bot {settings.discord_bot_token}"}

    # 디엠방을 파거나 찾는 메서드
    async def _open_dm_channel(self, discord_user_id: str) -> str:
        response = await self._client.post(
            f"{DISCORD_API_BASE}/users/@me/channels",
            json={"recipient_id": discord_user_id},
            headers=self._headers()
        )
        response.raise_for_status()
        return response.json()["id"]

    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError, TransientWebhookError),
    )
    async def send_dm(self, discord_user_id: str, payload: dict) -> None:
        channel_id = await self._open_dm_channel(discord_user_id)
        response = await self._client.post(
            f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
            json=payload,
            headers=self._headers(),
        )

        if response.status_code in (200, 201):
            return
        elif response.status_code == 429:
            raise TransientWebhookError("rate limited (429)")
        elif 400 <= response.status_code < 500:
            raise PermanentWebhookError(f"permanent error {response.status_code}")
        else:
            raise TransientWebhookError(f"server error {response.status_code}")