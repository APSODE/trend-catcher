import httpx
import json

class ExtractionService:
    URL = "https://integrate.api.nvidia.com/v1/chat/completions"
    MODEL = "nvidia/nemotron-3-nano-30b-a3b"
    TIMEOUT = 300

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient()

    #메인 기능
    #정상 작동시 dict, 오류 시 None 리턴
    #네트워크/http 에러는 예외처리
    async def extract(self, title:str, content: str) -> dict | None:
        prompt = f"""
        다음 뉴스 기사를 읽고, 아래 지침에 따라 핵심 키워드와 주제, 신뢰도를 추출해줘
        
        #지침
        - keywords는 기사의 핵심 명사(인물, 기관, 사건명 등) 2~3개
        - topic은 이 기사가 다루는 구체적인 사건/이슈를 한 문장으로
        - content_score는 이 기사가 얼마나 사실 위주로 작성되었는지 0.0 ~ 1.0으로 평가 (구체적 수치, 기관명, 인용이 있으면 높게, 추측성 표현이 많으면 낮게)
        - 반드시 아래 형식의 JSON만 출력할 것. 설명이나 다른 텍스트 덧붙이기 절대 금지
        
        #출력양식
        {{"keywords": ["금리", "한국은행"], "topic": "한국은행이 기준금리를 동결했다", "content_score": 0.8}}
        
        #기사
        제목: {title}
        본문: {content}
        """

        headers = {
            "Authorization" : f"Bearer {self.api_key}",
            "Content-Type" : "application/json"
        }
        payload = {
            "model" : self.MODEL,
            "messages" : [{"role" : "user", "content" : prompt}],
            "max_tokens" : 300,
            "chat_template_kwargs" : {"enable_thinking" : False}
        }

        response = await self.client.post(self.URL, headers = headers, json = payload, timeout = self.TIMEOUT)
        print(response.status_code, response.text)  # TODO: 디버깅용 코드, 제거필요
        response.raise_for_status()  # 당신 에러인가
        raw = response.json()["choices"][0]["message"]["content"].strip()

        if raw.startswith("```"): #당신 ```으로 포장되어있는가
            raw = raw.split("```")[1].removeprefix("json").strip()

        try:
            result = json.loads(raw) #당신을 포장하겠소
        except json.JSONDecodeError: #당신 json이 아닌가
            return None

        if not all(k in result for k in ("keywords", "topic", "content_score")): #당신 구성이 잘못되었나
            return None
        if not isinstance(result["keywords"], list): #당신 리스트 맞나
            return None
        if not isinstance(result["content_score"], (int, float)): #당신 점수 숫자 맞나
            return None
        return result #모든 검증을 통과한 당신 출발

    async def close(self):
        await self.client.aclose()