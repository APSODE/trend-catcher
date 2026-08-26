from typing import NewType
from hashlib import sha256
from os import urandom
from src.user_api.config import account_config
from src.user_api.exceptions import IllegalSaltException

HashedString = NewType("HashedString", str)


class HashUtil:
    @staticmethod
    def create_salt(length: int) -> str:
        if account_config.MIN_SALT_LENGTH <= length <= account_config.MAX_SALT_LENGTH:
            return sha256(urandom(length)).hexdigest()

        else:
            raise IllegalSaltException(
                length = length,
                min_length = account_config.MIN_SALT_LENGTH,
                max_length = account_config.MAX_SALT_LENGTH
            )



    @staticmethod
    def get_hashed_string(target: str, salt: str) -> HashedString:
        return HashedString(sha256(f"{target}{salt}".encode()).hexdigest())
