from enum import Enum

class AccountProvider(str, Enum):
    DISCORD = "discord"

class AccountType(str, Enum):
    LOCAL = "local"
    SOCIAL = "social"


LOCAL = AccountType.LOCAL
SOCIAL = AccountType.SOCIAL
DISCORD = AccountProvider.DISCORD

__all__ = [
    "AccountProvider",
    "AccountType",
    "LOCAL",
    "SOCIAL",
    "DISCORD",
]
