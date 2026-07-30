from typing import NewType
from hashlib import sha256
from os import urandom
from src.user_api.constant.account_constant import MIN_SALT_LENGTH, MAX_SALT_LENGTH
from src.user_api.exceptions.hash_exceptions import IllegalSaltException

HashedString = NewType("HashedString", str)

class HashUtil:
    @staticmethod
    def create_salt(length: int) -> str:
        if MIN_SALT_LENGTH <= length <= MAX_SALT_LENGTH:
            return sha256(urandom(length)).hexdigest()

        else:
            raise IllegalSaltException(length = length, min_length = MIN_SALT_LENGTH, MAX_SALT_LENGTH = MAX_SALT_LENGTH)



    @staticmethod
    def get_hashed_string(target: str, salt: str) -> HashedString:
        return HashedString(sha256(f"{target}{salt}".encode()).hexdigest())




