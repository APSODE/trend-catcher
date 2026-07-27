from hashlib import sha256
from os import urandom

from src.user_api.constant.user_model_constant import MIN_SALT_LENGTH, MAX_SALT_LENGTH
from src.user_api.exceptions.hash_exceptions import IllegalSaltException


class StringHashService:
    @staticmethod
    async def create_salt(length: int) -> str:
        if MIN_SALT_LENGTH <= length <= MAX_SALT_LENGTH:
            return sha256(urandom(length)).hexdigest()

        else:
            raise IllegalSaltException(length = length, min_length = MIN_SALT_LENGTH, MAX_SALT_LENGTH = MAX_SALT_LENGTH)



    @staticmethod
    async def get_hashed_password(raw_password: str, salt: str) -> str:



