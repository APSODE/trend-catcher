from src.crawler_api.exception.base_error_exception import BaseErrorException

class NotFoundException(BaseErrorException):
    def __init__(self, message : str | None = None):
        if message:
            super().__init__(message)
        else:
            super().__init__("데이터를 찾지 못했습니다")
