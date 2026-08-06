from fastapi import HTTPException

class BaseErrorException(HTTPException):
    def __init__(self, message : str | None = None, status_code : int = 404):
        if message:
            super().__init__(detail = message, status_code = status_code)
        else:
            super().__init__(detail = "오류 발생", status_code = status_code)

