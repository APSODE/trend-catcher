import asyncio
from src.llm_api.constant.nvidia_constant import LLMConstant
from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.schema.extraction import ExtractionResultData
from src.llm_api.exception.parse_exception import JsonParseException
from src.llm_api.util.json_util import JsonUtil
import logging

logger = logging.getLogger(__name__)

class ExtractionService:
    def __init__(self, client: NvidiaClient):
        self._client = client

    #추출
    async def extract(self, title: str, content: str) -> ExtractionResultData:
        prompt = LLMConstant.EXTRACTION_PROMPT_TEMPLATE.format(title = title, content = content)

        for attempt in range(LLMConstant.EXTRACTION_RETRY_ATTEMPTS):
            try:
                raw_response = await self._client.chat_completion(prompt)
                return JsonUtil.parse(raw_response, ExtractionResultData)
            except JsonParseException:
                if attempt == LLMConstant.EXTRACTION_RETRY_ATTEMPTS - 1:
                    raise
                logger.warning("추출 실패, 재시도 (%d회차)", attempt + 1)
                await asyncio.sleep(LLMConstant.RETRY_BASE_DELAY)
        raise RuntimeError("추출 재시도 횟수 설정 잘못됨")