from pydantic import Field

from src.user_api.config.base_config import BaseConfig


class DatabaseConfig(BaseConfig):
    oracle_id: str = Field(validation_alias = "ORACLE_DB_ID")
    oracle_pw: str = Field(validation_alias = "ORACLE_DB_PW")
    redis_pw: str = Field(validation_alias = "REDIS_DB_PW")
