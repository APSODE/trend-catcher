import httpx

from src.sns_api.config import get_settings
from src.sns_api.decorator.retry import async_retry
from src.sns_api.model.schema_model import NewsBundleData, NewsItemData
settings = get_settings()

DISCORD_API_BASE = "https://discord.com/api/v10"

EMBED_FIELD_VALUE_LIMIT = 1024
MAX_ITEMS_PER_FIELD = 10

# 슬롯별 컬러/문구
SLOT_STYLE = {
    "아침": {"color": 0xFFA552, "emoji": "☀️", "greeting": "상쾌한 아침, 오늘의 소식을 확인해보세요!"},
    "저녁": {"color": 0x6C63FF, "emoji": "🌙", "greeting": "하루를 마무리하며, 놓친 소식은 없는지 확인해보세요!"},
}
DEFAULT_STYLE = {"color": 0x5865F2, "emoji": "📰", "greeting": "오늘의 소식을 확인해보세요!"}


class TransientWebhookError(Exception):
    """일시적 실패 - 재시도 대상"""


class PermanentWebhookError(Exception):
    """영구적 실패 - 재시도하지 않음"""


def _build_lines(items: list[NewsItemData]) -> tuple[str, str | None]:
    lines = []
    thumbnail_url = None
    for i, item in enumerate(items[:MAX_ITEMS_PER_FIELD], start=1):
        title = item.title.replace("[", "(").replace("]", ")")  # 마크다운 깨짐 방지
        line = f"{i}. [{title}]({item.url})"
        lines.append(line)
        if thumbnail_url is None and item.image_url:
            thumbnail_url = item.image_url

    value = "\n".join(lines)
    if len(value) > EMBED_FIELD_VALUE_LIMIT:
        value = value[: EMBED_FIELD_VALUE_LIMIT - 3] + "..."  # 길이 초과 시 안전하게 자름

    return value, thumbnail_url


# 디스코드 디엠 메세지 내용
def build_payload(bundle: NewsBundleData, slot_label: str) -> dict:
    field = []
    thumbnail_url = None

    # 주요 뉴스 내용상자
    if bundle.major:
        value, thumb = _build_lines(bundle.major)
        field.append({"name": "🔥 주요 뉴스", "value": value})
        if thumbnail_url is None:
            thumbnail_url = thumb

    # 개인화된 뉴스 내용상자
    if bundle.personalized:
        value, thumb = _build_lines(bundle.personalized)
        field.append({"name": "✨ 사용자 맞춤 뉴스", "value": value})
        if thumbnail_url is None:
            thumbnail_url = thumb

    style = SLOT_STYLE.get(slot_label, DEFAULT_STYLE)

    embed: dict[str, object] = {
        "title": f"{style['emoji']} {slot_label} 뉴스 브리핑",
        "description": style["greeting"],
        "color": style["color"],
        "fields": field,
    }
    if thumbnail_url:
        embed["thumbnail"] = {"url": thumbnail_url}

    return {
        "username": "Trend Catcher",
        "embeds": [embed],
    }


class DiscordClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @staticmethod
    def _headers() -> dict:
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

    # 주요 뉴스 -> 메인 서버를 두고 채널 전송
    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError, TransientWebhookError),
    )
    async def send_to_channel(self, channel_id: str, payload: dict) -> None:
        response = await self._client.post(
            f"{DISCORD_API_BASE}/channels/{channel_id}/messages",
            json=payload,
            headers=self._headers(),
        )
        self._handle_response(response)

    # 개인화된 뉴스 -> DM 전송
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
        self._handle_response(response)

    @staticmethod
    def _handle_response(response) -> None:
        if response.status_code in (200, 201):
            return
        elif response.status_code == 429:
            raise TransientWebhookError("rate limited (429)")
        elif 400 <= response.status_code < 500:
            raise PermanentWebhookError(f"permanent error {response.status_code}")
        else:
            raise TransientWebhookError(f"server error {response.status_code}")