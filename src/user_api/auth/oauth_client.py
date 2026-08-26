from dataclasses import dataclass
from typing import Dict

import httpx

from src.user_api.constant.account_constant import AccountProvider
from src.user_api.dto import OAuth2Response
from src.user_api.exceptions.account_exceptions import UnsupportedProvider
from src.user_api.exceptions.auth_exceptions import InvalidToken

@dataclass
class OAuth2ProviderConfig:
    provider: AccountProvider
    user_info_url: str
    id_field: str
    name_field: str | None = None

class OAuth2Client:
    _registry: Dict[AccountProvider, "OAuth2Client"] = {}
    _http_client = httpx.AsyncClient()

    def __init__(self, config: OAuth2ProviderConfig):
        self._config = config

    @classmethod
    async def close(cls) -> None:
        if cls._http_client is not None:
            await cls._http_client.aclose()
            cls._http_client = None

    async def fetch_user_info(self, access_token: str) -> OAuth2Response:

        response = await self._http_client.get(
            self._config.user_info_url,
            headers = {"Authorization": f"Bearer {access_token}"},
        )

        if response.status_code != 200:
            raise InvalidToken()

        data = response.json()

        return OAuth2Response(
            provider = self._config.provider,
            provider_user_id = data.get(self._config.id_field),
            name = data.get(self._config.name_field) if self._config.name_field is not None else None
        )

    @classmethod
    def register(cls, provider: AccountProvider, config: OAuth2ProviderConfig) -> None:
        cls._registry[provider] = cls(config)

    @classmethod
    def get_client(cls, provider: AccountProvider) -> "OAuth2Client":
        client = cls._registry.get(provider)
        if client is None:
            # 기존에는 순수 ValueError를 던져서 AppException 체계(및 통합 핸들러)를
            # 벗어나 처리되지 않은 500으로 나갔음. 클라이언트가 잘못된 provider 값을
            # 보낸 상황이므로 400번대 전용 예외로 교체함.
            raise UnsupportedProvider(provider)
        return client


OAuth2Client.register(
    AccountProvider.DISCORD,
    OAuth2ProviderConfig(
        provider = AccountProvider.DISCORD,
        user_info_url = "https://discord.com/api/users/@me",
        id_field = "id",
        name_field = "username",
    ),
)
