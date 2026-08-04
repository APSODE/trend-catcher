from src.user_api.exceptions.hashtag_exception import UnknownHashtagData
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler, E


class UnknownHashtagDataExceptionHandler(BaseExceptionHandler[UnknownHashtagData]):
    def __init__(self):
        super().__init__(UnknownHashtagData)