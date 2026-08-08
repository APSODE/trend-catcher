from pydantic import BaseModel
from typing import TypeVar, Type
import json
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

DataType = TypeVar("DataType", bound = BaseModel) #타입체크 방지턱

class JsonUtil:
    #응답 파싱
    @staticmethod
    def parse(raw_response: str, datatype: Type[DataType]) -> DataType:
        cleaned_response = JsonUtil._clean_raw_response(raw_response)
        try:
            data = json.loads(cleaned_response) #포장
        except json.JSONDecodeError:
            logger.warning("LLM 응답 JSON 파싱 실패. 원본: %s", raw_response[:200]) #원본 응답 기록
            raise

        try:
            return datatype.model_validate(data) #스키마 검증 후 리턴
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