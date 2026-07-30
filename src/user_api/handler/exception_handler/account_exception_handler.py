from src.user_api.exceptions.account_exceptions import IsAlreadyExistLoginID, InvalidCredentialData
from src.user_api.handler.exception_handler.base_exception_handler import BaseExceptionHandler


class IsAlreadyExistLoginIDHandler(BaseExceptionHandler):
    def __init__(self):
        super().__init__(IsAlreadyExistLoginID.status_code)



class InvalidCredentialDataHandler(BaseExceptionHandler):
    def __init__(self):
        super().__init__(InvalidCredentialData.status_code)




