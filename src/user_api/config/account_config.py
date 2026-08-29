from pydantic import Field
from src.user_api.config.base_config import BaseConfig


class AccountConfig(BaseConfig):
    MAX_ID_LENGTH: int = Field(validation_alias = "ACCOUNT_MAX_ID_LENGTH")
    MAX_PW_LENGTH: int = Field(validation_alias = "ACCOUNT_MAX_PW_LENGTH")
    MAX_SALT_LENGTH: int = Field(validation_alias = "ACCOUNT_MAX_SALT_LENGTH")
    MIN_SALT_LENGTH: int = Field(validation_alias = "ACCOUNT_MIN_SALT_LENGTH")

    SALT_LENGTH: int = Field(validation_alias = "ACCOUNT_SALT_LENGTH")









