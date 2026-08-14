import httpx
from pydantic import SecretStr
from src.llm_api.constant.nvidia_constant import LLMConstant, EmbeddingInputType
from src.llm_api.exception.external_exception import NvidiaApiException
from src.llm_api.infrastructure.base_api_client import BaseApiClient
import logging

logger = logging.getLogger(__name__)

class NvidiaClient(BaseApiClient):
    def __init__(self, client: httpx.AsyncClient, api_key: SecretStr):
        super().__init__(
            client = client,
            base_url = LLMConstant.BASE_URL,
            exception_class = NvidiaApiException,
            retry_attempts = LLMConstant.HTTP_RETRY_ATTEMPTS,
            retry_base_delay = LLMConstant.RETRY_BASE_DELAY,
            default_headers = {
            "Authorization" : f"Bearer {api_key.get_secret_value()}",
            "Content-Type" : "application/json"
            }
        )

    #LLM 응답
    async def chat_completion(self, prompt: str) -> str:
        payload = {
            "model" : LLMConstant.EXTRACTION_MODEL,
            "messages" : [{"role" : "user", "content" : prompt}]
        }
        response = await self._post(LLMConstant.EXTRACTION_PATH, LLMConstant.EXTRACTION_TIMEOUT, payload)
        return response["choices"][0]["message"]["content"]

    #임베딩 응답
    async def create_embedding(self, text:str, input_type: EmbeddingInputType) -> list[float]:
        embeddings = await self.create_embeddings([text], input_type)
        return embeddings[0]
    
    #여러 임베딩 응답
    async def create_embeddings(self, texts:list[str], input_type: EmbeddingInputType) -> list[list[float]]:
        payload = {
            "model": LLMConstant.EMBEDDING_MODEL,
            "input": texts,
            "input_type": input_type
        }
        response = await self._post(LLMConstant.EMBEDDING_PATH, LLMConstant.EMBEDDING_TIMEOUT, payload)
        return [item["embedding"] for item in response["data"]]