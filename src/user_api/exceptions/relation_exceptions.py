from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class NotFollowedHashtagData(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__(f"Current hashtag is unfollowed")