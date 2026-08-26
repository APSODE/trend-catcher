from pydantic import Field

from src.user_api.config.base_config import BaseConfig


class ModelConfig(BaseConfig):
    MAX_NAME_LENGTH: int = Field(validation_alias = "USER_MAX_NAME_LENGTH")