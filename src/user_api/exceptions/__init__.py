from src.user_api.exceptions.app_exception import AppException

from src.user_api.exceptions.account_exceptions import (
    IsAlreadyExistLoginID,
    InvalidCredentialData,
    NotExistAccountData,
    AlreadyLinkedAccount,
    AlreadyLinkedProvider,
    AlreadyOwnAccount,
    UnlinkedSocialAccount,
    UnsupportedProvider,
    CannotUnlinkLastLoginMethod,
    DeleteConfirmationMismatch,
)
from src.user_api.exceptions.auth_exceptions import InvalidToken, ExpiredToken, MismatchTokenType
from src.user_api.exceptions.hash_exceptions import IllegalSaltException
from src.user_api.exceptions.hashtag_exception import UnknownHashtagData, InvalidHashtagAmount, InvalidHashtagNameLength
from src.user_api.exceptions.internal_exceptions import (
    SerializerNotRegistered,
    SerializerTypeMismatch,
    UnexpectedNullSerializeTarget,
)
from src.user_api.exceptions.relation_exceptions import NotFollowedHashtagData, AlreadyFollowedHashtagData
from src.user_api.exceptions.user_exceptions import UnknownUserData

__all__ = [
    "AppException",
    "IsAlreadyExistLoginID",
    "InvalidCredentialData",
    "NotExistAccountData",
    "AlreadyLinkedAccount",
    "AlreadyLinkedProvider",
    "AlreadyOwnAccount",
    "UnlinkedSocialAccount",
    "UnsupportedProvider",
    "CannotUnlinkLastLoginMethod",
    "DeleteConfirmationMismatch",
    "InvalidToken",
    "ExpiredToken",
    "MismatchTokenType",
    "IllegalSaltException",
    "UnknownHashtagData",
    "InvalidHashtagAmount",
    "InvalidHashtagNameLength",
    "SerializerNotRegistered",
    "SerializerTypeMismatch",
    "UnexpectedNullSerializeTarget",
    "NotFollowedHashtagData",
    "AlreadyFollowedHashtagData",
    "UnknownUserData",
]
