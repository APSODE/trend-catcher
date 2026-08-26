from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class NotFollowedHashtagData(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__(
            "Current hashtag is unfollowed",
            error_code = "HASHTAG_NOT_FOLLOWED",
        )


class AlreadyFollowedHashtagData(AppException):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self):
        super().__init__(
            "Current hashtag already followed",
            error_code = "HASHTAG_ALREADY_FOLLOWED",
        )
