from http.client import HTTPException


class FetchValueException(HTTPException):
    def __init__(self, message : str | None = None):
        self.status_code = 404
        if message:
            super().__init__(message)
        else:
            super().__init__("Fetch 과정에서 문제가 발생했습니다")

