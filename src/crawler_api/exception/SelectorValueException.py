from http.client import HTTPException


class SelectorValueException(HTTPException):
    def __init__(self, message : str | None = None):
        self.status_code = 404
        if message:
            super().__init__(message)
        else:
            super().__init__("언론사 데이터의 셀렉터나 Base Url이 누락됐습니다")