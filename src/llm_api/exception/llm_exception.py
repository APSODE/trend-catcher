class LLMServiceException(Exception):
    status_code: int = 500

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

#외부 서비스 api 호출 실패
class ExternalApiException(LLMServiceException):
    status_code: int = 502

#nvidia api 호출 실패
class NvidiaApiException(ExternalApiException):
    pass

#외부에서 받은 데이터 파싱 실패
class DataParseException(LLMServiceException):
    status_code = 502

#JSON문법 오류
class JsonParseException(DataParseException):
    pass

#이거없는데??
class ResourceNotFoundException(LLMServiceException):
    status_code = 404


