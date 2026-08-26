from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class IsAlreadyExistLoginID(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self, login_id: str):
        super().__init__(f"login id : [{login_id}] is already exist.")


class InvalidCredentialData(AppException):
    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(self):
        super().__init__("Invalid username or password")


class NotExistAccountData(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__("Not exist data, please check data")


class AlreadyLinkedAccount(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__("already linked other account")


class AlreadyLinkedProvider(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__("already linked account provider")


class AlreadyOwnAccount(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__("already linked own account")


class UnlinkedSocialAccount(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__("Unlinked social account")


class UnsupportedProvider(AppException):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, provider):
        super().__init__(f"Unsupported provider: {provider}")


class CannotUnlinkLastLoginMethod(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__("Cannot unlink the last social login method when there is no local account.")


class DeleteConfirmationMismatch(AppException):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self):
        super().__init__("The entered name does not match your account information.")
