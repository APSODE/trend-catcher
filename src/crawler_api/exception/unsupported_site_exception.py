from src.crawler_api.exception.base_error_exception import BaseErrorException

class UnsupportedSiteException(BaseErrorException):
    def __init__(self, message : str | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("아직 지원되지않는 언론사 입니다")