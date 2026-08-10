import httpx
import asyncio
from pydantic import SecretStr
from src.llm_api.constant.llm_constant import LLMConstant
from src.llm_api.exception.llm_exception import NvidiaApiException
import logging

logger = logging.getLogger(__name__)

class NvidiaClient:
    def __init__(self, client: httpx.AsyncClient, api_key: SecretStr):
        self._client = client
        self._api_key = api_key

    #LLM 응답
    async def chat_completion(self, prompt: str) -> str:
        payload = {
            "model" : LLMConstant.EXTRACTION_MODEL,
            "messages" : [{"role" : "user", "content" : prompt}]
        }
        response = await self._post_with_retry(LLMConstant.EXTRACTION_URL, payload, LLMConstant.EXTRACTION_TIMEOUT)
        return response["choices"][0]["message"]["content"]

    #임베딩 응답
    async def create_embedding(self, text:str, input_type: str) -> list[float]:
        embeddings = await self.create_embeddings([text], input_type)
        return embeddings[0]
    
    #여러 임베딩 응답
    async def create_embeddings(self, texts:list[str], input_type: str) -> list[list[float]]:
        payload = {
            "model": LLMConstant.EMBEDDING_MODEL,
            "input": texts,
            "input_type": input_type
        }
        response = await self._post_with_retry(LLMConstant.EMBEDDING_URL, payload, LLMConstant.EMBEDDING_TIMEOUT)
        return [item["embedding"] for item in response["data"]]

    #재시도
    async def _post_with_retry(self, url: str, payload: dict, timeout: int) -> dict:
        for attempt in range(LLMConstant.HTTP_RETRY_ATTEMPTS):
            try:
                response = await self._client.post(url, headers = self._get_headers(), json = payload, timeout = timeout)
                response.raise_for_status()
                return response.json()
            except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError) as error:
                if attempt == LLMConstant.HTTP_RETRY_ATTEMPTS - 1:
                    raise NvidiaApiException(f"NVIDIA API 호출 실패: {url}") from error
                delay = LLMConstant.RETRY_BASE_DELAY * (2 ** attempt)
                logger.warning("API 호출 실패, 재시도 (%d회차, %.1f초 후)", attempt + 1, delay)
                await asyncio.sleep(delay)
        raise RuntimeError("HTTP 재시도 횟수 설정 잘못됨")

    #헤더 반환 헬퍼
    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization" : f"Bearer {self._api_key.get_secret_value()}",
            "Content-Type" : "application/json"
        }