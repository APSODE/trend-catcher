from http.client import HTTPException


class SelectorValueException(HTTPException):
    def __init__(self):
        super().__init__("언론사 데이터의 셀렉터나 Base Url이 누락됐습니다")
        self.status_code = 404