from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


ENV_PATH = Path(__file__).resolve().parents[1] / "url.env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Infra API"

    user_api_url : str = Field(validation_alias="USER_API_URL")
    sns_api_url : str = Field(validation_alias="SNS_API_URL")
    crawler_api_url : str = Field(validation_alias="CRAWLER_API_URL")
    llm_api_url : str = Field(validation_alias="LLM_API_URL")

    frontend_origins: str = Field(validation_alias="FRONTEND_ORIGINS")

    default_timeout : float = 10.0
    llm_api_timeout : float = 30.0

@lru_cache
def get_settings() -> Settings:
    return Settings(
        # user_api_url = "100.94.34.103:5175",
        # sns_api_url = "100.107.191.107:8080",
        # crawler_api_url = ""
    )
