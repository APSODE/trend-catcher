from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class UnknownHashtagData(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__(
            "An error occurred while retrieving hashtag information. Please try again.",
            error_code = "HASHTAG_NOT_FOUND",
        )


class InvalidHashtagAmount(AppException):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self):
        super().__init__(
            "Invalid hashtag amount",
            error_code = "HASHTAG_INVALID_AMOUNT",
        )


class InvalidHashtagNameLength(AppException):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, length: int, max_length: int):
        super().__init__(
            f"Hashtag name length {length} exceeds the maximum allowed length of {max_length}.",
            error_code = "HASHTAG_INVALID_NAME_LENGTH",
        )
