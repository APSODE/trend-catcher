from pydantic import BaseModel
from typing import TypeVar, Type
import json
from pydantic import ValidationError
from src.llm_api.exception.parse_exception import JsonParseException
import logging

logger = logging.getLogger(__name__)

DataType = TypeVar("DataType", bound = BaseModel) #타입체크 방지턱

class JsonUtil:
    #응답 파싱
    @staticmethod
    def parse(raw_response: str, data_class: Type[DataType]) -> DataType:
        cleaned_response = JsonUtil._clean_raw_response(raw_response)
        try:
            data = json.loads(cleaned_response) #포장
        except json.JSONDecodeError as error:
            logger.warning("LLM 응답 JSON 파싱 실패. 원본: %s", raw_response[:200]) #원본 응답 기록
            raise JsonParseException("LLM 응답이 JSON 형식이 아님") from error

        try:
            return data_class.model_validate(data) #스키마 검증 후 리턴
        except ValidationError as error:
            logger.warning("LLM 응답 형식 오류. data: %s", cleaned_response[:200])
            raise JsonParseException("LLM 응답이 요구되는 형식과 맞지 않음") from error

    #응답 청소 후 포장
    @staticmethod
    def _clean_raw_response(response: str) -> str:
        response = response.strip() #양끝 공백 제거
        if response.startswith("```"):
            response = response.split("```")[1].removeprefix("json").strip() #``` 지우고 접두사 json 떼낸 뒤 다시 공백제거
        return response