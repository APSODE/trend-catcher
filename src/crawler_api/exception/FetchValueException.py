from http.client import HTTPException


class FetchValueException(HTTPException):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 404