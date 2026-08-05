from src.user_api.exceptions.user_exceptions import UnknownUserData
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler


class UnknownUserDataExceptionHandler(BaseExceptionHandler[UnknownUserData]):
    def __init__(self):
        super().__init__(UnknownUserData)