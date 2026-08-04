from typing import Type

from src.user_api.exceptions.relation_exceptions import NotFollowedHashtagData
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler, E


class NotFollowedHashtagExceptionHandler(BaseExceptionHandler[NotFollowedHashtagData]):
    def __init__(self):
        super().__init__(NotFollowedHashtagData)