from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class UnknownUserData(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__("An error occurred while retrieving user information. Please try again.")
