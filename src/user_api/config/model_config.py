from pydantic import Field

from src.user_api.config.base_config import BaseConfig


class ModelConfig(BaseConfig):
    USER_MAX_NAME_LENGTH: int = Field(validation_alias = "USER_MAX_NAME_LENGTH")
    HASHTAG_MAX_NAME_LENGTH: int = Field(validation_alias = "HASHTAG_MAX_NAME_LENGTH")
