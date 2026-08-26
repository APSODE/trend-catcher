from typing import Optional

from src.user_api.exceptions.app_exception import AppException


class IllegalSaltException(AppException):
    def __init__(self, length: int, min_length: Optional[int] = None, max_length: Optional[int] = None):
        if min_length is not None and max_length is not None:
            message = (
                f"The salt length {length} is invalid. "
                f"It must be between {min_length} and {max_length} characters."
            )
        else:
            message = f"The provided salt length {length} is outside the allowed range."

        super().__init__(message)
