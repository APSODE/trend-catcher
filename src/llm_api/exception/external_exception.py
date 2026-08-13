from src.llm_api.exception.base_exception import LLMServiceException

#외부 api 호출 실패
class ExternalApiException(LLMServiceException):
    status_code = 502

#엔비디아
class NvidiaApiException(ExternalApiException):
    pass

#크롤러
class CrawlerApiException(ExternalApiException):
    pass

#유저
class UserApiException(ExternalApiException):
    pass