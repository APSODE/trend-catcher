from src.crawler_api.exception.base_error_exception import BaseErrorException

class CreateErrorException(BaseErrorException):
    def __init__(self, message : str | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("생성 과정에서 오류가 발생했습니다")

