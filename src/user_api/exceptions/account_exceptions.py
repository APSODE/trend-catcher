from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class IsAlreadyExistLoginID(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self, login_id: str):
        super().__init__(f"login id : [{login_id}] is already exist.")

class InvalidCredentialData(AppException):
    status_code = HTTPStatus.NOT_FOUND
    def __init__(self):
        super().__init__("Invalid username or password")

class UnknownAccountData(AppException):
    status_code = HTTPStatus.NOT_FOUND
    def __init__(self):
        super().__init__("unknown account data, please check data")