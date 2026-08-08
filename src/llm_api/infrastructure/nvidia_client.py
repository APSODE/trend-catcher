import httpx
from pydantic import SecretStr
from src.llm_api.constant.llm_constant import LLMConstant

class NvidiaClient:
    def __init__(self, client: httpx.AsyncClient, api_key: SecretStr):
        self._client = client
        self._api_key = api_key

    #LLM 응답
    async def chat_completion(self, prompt: str) -> str:
        headers = self._get_headers()
        payload = {
            "model" : LLMConstant.EXTRACTION_MODEL,
            "messages" : [{"role" : "user", "content" : prompt}]
        }
        response = await self._client.post(LLMConstant.EXTRACTION_URL, headers = headers, json = payload, timeout = LLMConstant.EXTRACTION_TIMEOUT)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    #임베딩 응답
    async def create_embedding(self, text:str, input_type: str) -> list[float]:
        embeddings = await self.create_embeddings([text], input_type)
        return embeddings[0]
    
    #여러 임베딩 응답
    async def create_embeddings(self, texts:list[str], input_type: str) -> list[list[float]]:
        headers = self._get_headers()
        payload = {
            "model": LLMConstant.EMBEDDING_MODEL,
            "input": texts,
            "input_type": input_type
        }
        response = await self._client.post(LLMConstant.EMBEDDING_URL, headers = headers, json = payload, timeout = LLMConstant.EMBEDDING_TIMEOUT)
        response.raise_for_status()
        items = sorted(response.json()["data"], key=lambda x: x["index"])
        return [item["embedding"] for item in items]

    #헤더 반환 헬퍼
    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization" : f"Bearer {self._api_key.get_secret_value()}",
            "Content-Type" : "application/json"
        }