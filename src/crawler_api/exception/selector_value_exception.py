from src.crawler_api.exception.base_error_exception import BaseErrorException


class SelectorValueException(BaseErrorException):
    def __init__(self, message: str | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("언론사 데이터의 셀렉터나 Base Url이 누락됐습니다")