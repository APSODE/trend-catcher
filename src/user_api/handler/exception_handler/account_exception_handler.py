from src.user_api.exceptions.account_exceptions import IsAlreadyExistLoginID, InvalidCredentialData
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler


class IsAlreadyExistLoginIDHandler(BaseExceptionHandler[IsAlreadyExistLoginID]):
    def __init__(self):
        super().__init__(IsAlreadyExistLoginID)   # 클래스 자체를 전달


class InvalidCredentialDataHandler(BaseExceptionHandler[InvalidCredentialData]):
    def __init__(self):
        super().__init__(InvalidCredentialData)