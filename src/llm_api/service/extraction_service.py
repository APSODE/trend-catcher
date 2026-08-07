import asyncio
import json
import logging

from src.llm_api.constant.llm_constant import LLMConstant
from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.schema.extraction import ExtractionResultData
from pydantic import ValidationError

logger = logging.getLogger(__name__)

class ExtractionService:

    def __init__(self, client: NvidiaClient):
        self._client = client

    #추출
    async def extract(self, title: str, content: str) -> ExtractionResultData:
        prompt = LLMConstant.PROMPT_TEMPLATE.format(title = title, content = content)

        for attempt in range(LLMConstant.EXTRACTION_RETRY_ATTEMPTS):
            try:
                raw_response = await self._client.chat_completion(prompt)
                return self._parse(raw_response)
            except (json.JSONDecodeError, ValidationError):
                if attempt == LLMConstant.EXTRACTION_RETRY_ATTEMPTS - 1:
                    raise
                logger.warning("추출 실패, 재시도 (%d회차)", attempt + 1)
                await asyncio.sleep(LLMConstant.RETRY_BASE_DELAY)
        raise RuntimeError("추출 재시도 횟수 설정이 잘못됨")

    #응답 파싱
    def _parse(self, raw_response: str) -> ExtractionResultData:
        cleaned_response = ExtractionService._clean_raw_response(raw_response)
        try:
            data = json.loads(cleaned_response) #포장
        except json.JSONDecodeError:
            logger.warning("LLM 응답 JSON 파싱 실패. 원본: %s", raw_response[:200]) #원본 응답 기록
            raise

        try:
            return ExtractionResultData.model_validate(data) #스키마 검증 후 리턴
        except ValidationError:
            logger.warning("LLM 응답 형식 오류. data: %s", cleaned_response[:200])
            raise

    #응답 청소 후 포장
    @staticmethod
    def _clean_raw_response(response: str) -> str:
        response = response.strip() #양끝 공백 제거
        if response.startswith("```"):
            response = response.split("```")[1].removeprefix("json").strip() #``` 지우고 접두사 json 떼낸 뒤 다시 공백제거
        return response