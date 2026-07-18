from http.client import HTTPException


class UnsupportedSiteException(HTTPException):
    def __init__(self, message : str | None = None):
        self.status_code = 404
        if message:
            super().__init__(message)
        else:
            super().__init__("아직 지원되지않는 언론사 입니다")