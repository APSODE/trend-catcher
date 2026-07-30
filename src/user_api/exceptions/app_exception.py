from http import HTTPStatus

class AppException(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
