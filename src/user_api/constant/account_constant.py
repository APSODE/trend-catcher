from enum import Enum

class AccountProvider(str, Enum):
    DISCORD = "discord"

class AccountType(str, Enum):
    LOCAL = "local"
    SOCIAL = "social"



MAX_ID_LENGTH = 128
MAX_PW_LENGTH = 255
MAX_SALT_LENGTH = 255
MIN_SALT_LENGTH = 1


SALT_LENGTH = 10

LOCAL = AccountType.LOCAL
SOCIAL = AccountType.SOCIAL
DISCORD = AccountProvider.DISCORD

__all__ = [
    "MAX_ID_LENGTH",
    "MAX_PW_LENGTH",
    "MAX_SALT_LENGTH",
    "MIN_SALT_LENGTH",
    "SALT_LENGTH",
    "AccountProvider",
    "AccountType",
    "LOCAL",
    "SOCIAL",
    "DISCORD",
]