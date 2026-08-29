from src.llm_api.constant.api_constant import UserApiConstant
from src.llm_api.exception.external_exception import UserApiException
from src.llm_api.infrastructure.base_api_client import BaseApiClient
import httpx

class UserApiClient(BaseApiClient):
    def __init__(self, client: httpx.AsyncClient, base_url: str):
        super().__init__(
            client = client,
            base_url = base_url,
            exception_class = UserApiException,
            retry_attempts = UserApiConstant.RETRY_ATTEMPTS,
            retry_base_delay = UserApiConstant.RETRY_BASE_DELAY
        )

    #해시태그 전체 조회
    async def get_all_hashtags(self) -> list[str]:
        response = await self._get(UserApiConstant.HASHTAGS_PATH, UserApiConstant.TIMEOUT)
        return [item["name"] for item in response["datas"]]