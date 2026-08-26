from http import HTTPStatus

from src.user_api.exceptions.app_exception import AppException


class IsAlreadyExistLoginID(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self, login_id: str):
        super().__init__(
            f"login id : [{login_id}] is already exist.",
            error_code = "ACCOUNT_LOGIN_ID_ALREADY_EXISTS",
        )


class InvalidCredentialData(AppException):
    status_code = HTTPStatus.UNAUTHORIZED

    def __init__(self):
        super().__init__(
            "Invalid username or password",
            error_code = "ACCOUNT_INVALID_CREDENTIALS",
        )


class NotExistAccountData(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__(
            "Not exist data, please check data",
            error_code = "ACCOUNT_NOT_FOUND",
        )


class AlreadyLinkedAccount(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__(
            "already linked other account",
            error_code = "ACCOUNT_ALREADY_LINKED_OTHER_ACCOUNT",
        )


class AlreadyLinkedProvider(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__(
            "already linked account provider",
            error_code = "ACCOUNT_PROVIDER_ALREADY_LINKED",
        )


class AlreadyOwnAccount(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__(
            "already linked own account",
            error_code = "ACCOUNT_ALREADY_LINKED_OWN_ACCOUNT",
        )


class UnlinkedSocialAccount(AppException):
    status_code = HTTPStatus.NOT_FOUND

    def __init__(self):
        super().__init__(
            "Unlinked social account",
            error_code = "ACCOUNT_SOCIAL_NOT_LINKED",
        )


class UnsupportedProvider(AppException):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, provider):
        super().__init__(
            f"Unsupported provider: {provider}",
            error_code = "ACCOUNT_UNSUPPORTED_PROVIDER",
        )


class CannotUnlinkLastLoginMethod(AppException):
    status_code = HTTPStatus.CONFLICT

    def __init__(self):
        super().__init__(
            "Cannot unlink the last login method while no local account exists.",
            error_code = "ACCOUNT_CANNOT_UNLINK_LAST_LOGIN_METHOD",
        )


class DeleteConfirmationMismatch(AppException):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self):
        super().__init__(
            "The provided name does not match the account information.",
            error_code = "ACCOUNT_DELETE_CONFIRMATION_MISMATCH",
        )
