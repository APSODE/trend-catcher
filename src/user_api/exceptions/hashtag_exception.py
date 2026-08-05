from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class UnknownHashtagData(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__(f"An error occurred while retrieving hashtag information. Please try again.")



class InvalidHashtagAmount(AppException):
    status_code = HTTPStatus.BAD_REQUEST
    
    def __init__(self):
        super().__init__("Invalid hashtag amount")
