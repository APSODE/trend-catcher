import httpx
import numpy as np

class EmbeddingService:
    URL = "https://integrate.api.nvidia.com/v1/embeddings"
    MODEL = "nvidia/llama-nemotron-embed-1b-v2"
    HIGH_STANDARD = 0.75
    LOW_STANDARD = 0.5
    TIMEOUT = 30

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()

    async def get_embeddings(self, texts: list[str], input_type: str = "passage") -> list[list[float]]:
        headers = {
            "Authorization" : f"Bearer {self.api_key}",
            "Content-Type" : "application/json"
        }
        payload = {
            "input" : texts,
            "model" : self.MODEL,
            "input_type" : input_type
        }

        #주어라 내게 결과
        response = await self.client.post(self.URL, headers = headers, json = payload, timeout = self.TIMEOUT)  # 내놓아라 결과
        #print(response.status_code, response.text) #디버깅용 코드
        response.raise_for_status() #당신 에러인가
        data = response.json()["data"] #데이터만 통과
        data.sort(key = lambda x: x["index"]) #데이터 일렬로 줄서
        return [item["embedding"] for item in data]

    #유사도 비교
    def cosine_similarity(self, vec_a: list[float], vec_b: list[float]) -> float:
        a, b = np.array(vec_a), np.array(vec_b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    #점수 판별
    def classify_similarity(self, score: float) -> str:
        if score >= self.HIGH_STANDARD: #인가 당신 높은 점수 이상
            return "match"
        if score >= self.LOW_STANDARD: #인가 당신 낮은 점수 이상
            return "ambiguous"
        return "no_match" #당신 없다 매치되는 것

    async def close(self):
        await self.client.aclose()