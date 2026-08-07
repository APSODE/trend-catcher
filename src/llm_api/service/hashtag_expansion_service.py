import json
import asyncio
from src.llm_api.model.hashtag_model import HashtagModel
from src.llm_api.repository.hashtag_repository import HashtagRepository
from src.llm_api.infrastructure.nvidia_client import NvidiaClient
from src.llm_api.constant.llm_constant import LLMConstant, EmbeddingInputType
from src.llm_api.util.json_util import JsonUtil
from src.llm_api.schema.hashtag_expansion import HashtagExpansionData
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class HashtagExpansionService:
    def __init__(self, client: NvidiaClient, hashtag_repository: HashtagRepository):
        self._client = client
        self._hashtag_repository = hashtag_repository

    #받은거 싹 처리
    async def get_or_expand_all(self, hashtags: list[str]) -> list[HashtagModel]:
        if not hashtags:
            return []

        hashtags = self._normalize_all(hashtags)
        cached, unmatched = await self._filter_already_exist(hashtags)
        cached |= await self._expand_and_save_all(unmatched)

        return [cached[hashtag] for hashtag in hashtags]

    #정규화 후 중복 제거
    @staticmethod
    def _normalize_all(hashtags: list[str]) -> list[str]:
        normalized = [HashtagExpansionService._normalize(hashtag) for hashtag in hashtags]
        return list(dict.fromkeys(normalized))

    #이미 있는것들 걸러내기
    async def _filter_already_exist(self, hashtags: list[str]) -> tuple[dict[str, HashtagModel], list]:
        matched_list = await self._hashtag_repository.find_by_hashtags(hashtags)
        matched = {model.hashtag: model for model in matched_list}
        unmatched = [hashtag for hashtag in hashtags if hashtag not in matched]
        return matched, unmatched

    #정규화
    @staticmethod
    def _normalize(hashtag: str) -> str:
        return hashtag.strip().lstrip("#")

    #모두 확장 후 저장
    async def _expand_and_save_all(self, hashtags: list[str]) -> dict[str, HashtagModel]:
        result: dict[str, HashtagModel] = {}
        for hashtag in hashtags:
            result[hashtag] = await self._expand_and_save(hashtag)
        return result

    #확장 후 저장
    async def _expand_and_save(self, hashtag: str) -> HashtagModel:
        try:
            expansion = await self._expand(hashtag)
        except (json.JSONDecodeError, ValidationError): #TODO: 자체 예외를 던지고 받게 수정
            logger.warning("해시태그 확장 파싱 실패, 빈 확장 저장: %s", hashtag)
            expansion = HashtagExpansionData(aliases=[], children=[])
        except Exception:
            logger.exception("해시태그 확장 호출 실패, 빈 확장 저장: %s", hashtag)
            expansion = HashtagExpansionData(aliases=[], children=[])

        embedding = await self._client.create_embedding(hashtag, "query")
        return await self._hashtag_repository.create_hashtag(hashtag, expansion.aliases, expansion.children, embedding)

    #확장
    async def _expand(self, hashtag: str) -> HashtagExpansionData:
        prompt = LLMConstant.HASHTAG_PROMPT_TEMPLATE.format(hashtag = hashtag)

        for attempt in range(LLMConstant.HASHTAG_RETRY_ATTEMPTS):
            try:
                raw_response = await self._client.chat_completion(prompt)
                return JsonUtil.parse(raw_response, HashtagExpansionData)
            except (json.JSONDecodeError, ValidationError):
                if attempt == LLMConstant.HASHTAG_RETRY_ATTEMPTS - 1:
                    raise
                logger.warning("확장 실패, 재시도 (%d회차)", attempt + 1)
                await asyncio.sleep(LLMConstant.RETRY_BASE_DELAY)
        raise RuntimeError("확장 재시도 횟수 설정 잘못됨")
