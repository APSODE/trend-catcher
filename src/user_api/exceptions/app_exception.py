from http import HTTPStatus

class AppException(Exception):
    status_code = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

# class SerializeException(AppException):
#     def __init__(self, target_type: type, expected_type: type):
#         super().__init__(f"Expected type : {expected_type.__name__}, but target type is {target_type.__name__}")