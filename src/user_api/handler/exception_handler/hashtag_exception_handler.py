from src.user_api.exceptions.hashtag_exception import UnknownHashtagData
from src.user_api.exceptions.relation_exceptions import AlreadyFollowedHashtagData
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler


class UnknownHashtagDataExceptionHandler(BaseExceptionHandler[UnknownHashtagData]):
    def __init__(self):
        super().__init__(UnknownHashtagData)

class AlreadyFollowedHashtagDataExceptionHandler(BaseExceptionHandler[AlreadyFollowedHashtagData]):
    def __init__(self):
        super().__init__(AlreadyFollowedHashtagData)