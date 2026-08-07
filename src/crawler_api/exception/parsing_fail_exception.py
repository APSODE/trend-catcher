from src.crawler_api.exception.base_error_exception import BaseErrorException


class ParsingFailException(BaseErrorException):
    def __init__(self, message: str | None = None):
        if message:
            super().__init__("파싱 과정에서 문제가 발생했습니다\n"+message)
        else:
            super().__init__("파싱 과정에서 문제가 발생했습니다")
