from src.llm_api.exception.base_exception import LLMServiceException

#파싱 실패
class DataParseException(LLMServiceException):
    status_code = 502

#JSON문법오류 및 스키마 검증 실패
class JsonParseException(DataParseException):
    pass
