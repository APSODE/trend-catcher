from http.client import HTTPException


class FetchValueException(HTTPException):
    def __init__(self):
        super().__init__("Fetch 과정에서 문제가 발생했습니다")
        self.status_code = 404