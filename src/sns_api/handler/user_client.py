import httpx

from src.sns_api.config import get_settings
from src.sns_api.decorator.retry import async_retry

settings = get_settings()


class UserClient:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    # 유저id -> 디스코드 id
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

    # 디스코드 아이디 -> 우리 서비스의 user_id 역조회
    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError,),
    )
    async def get_user_id_by_discord_id(self, discord_user_id: str) -> int | None:
        response = await self._client.request(
            "GET",
            f"{settings.user_api_base_url}/internal/user-account/get-pk-by-provider-user-id",
            json={"provider_user_id": discord_user_id},
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        data = response.json()
        return data["pk"]

    # user_id -> 팔로우 해시태그 목록
    @async_retry(
        max_attempts=settings.http_max_retries,
        exceptions=(httpx.TransportError,),
    )
    async def get_user_hashtags(self, user_id: int) -> list[str]:
        response = await self._client.get(
            f"{settings.user_api_base_url}/internal/user/get-by-pk",
            params={"pk": user_id},
        )
        if response.status_code == 404:
            return []
        response.raise_for_status()
        data = response.json()
        return [h["name"] for h in data["interest"]]
