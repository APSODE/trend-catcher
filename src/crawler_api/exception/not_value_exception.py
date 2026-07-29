from src.crawler_api.exception.base_error_exception import BaseErrorException

class NotValueException(BaseErrorException):
    def __init__(self, message : str | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("값이 존재하지 않습니다")
