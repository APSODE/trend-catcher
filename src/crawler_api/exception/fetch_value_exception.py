from src.crawler_api.exception.base_error_exception import BaseErrorException


class FetchValueException(BaseErrorException):
    def __init__(self, message: str | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("Fetch 과정에서 문제가 발생했습니다")

