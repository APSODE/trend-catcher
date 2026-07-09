from http.client import HTTPException


class SelectorValueException(HTTPException):
    def __init__(self, message):
        super().__init__(message)
        self.status_code = 400