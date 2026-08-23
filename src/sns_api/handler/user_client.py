import httpx

from src.sns_api.config import get_settings
from src.sns_api.decorator.retry import async_retry

settings = get_settings()


class UserClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError,),
    )
    async def get_discord_user_id(self, user_id: int) -> str | None:
        response = await self._client.get(
            f"{settings.user_api_base_url}/internal/account/get-by-user-pk-and-provider",
            params={"user_pk": user_id, "provider": "DISCORD"},
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        # User의 소셜계정데이터 데이터들을 파이썬이 이해할 수 있게 변환
        data = response.json()
        return data["provider_user_id"]