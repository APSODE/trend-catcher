from pydantic import Field

from src.user_api.config.base_config import BaseConfig


class AuthConfig(BaseConfig):
    SECRET_KEY: str = Field(validation_alias = "JWT_SECRET_KEY")
    ALGORITHM: str = Field(validation_alias = "JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(validation_alias = "ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES: int = Field(validation_alias ="REFRESH_TOKEN_EXPIRE_MINUTES")
