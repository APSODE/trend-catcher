from functools import lru_cache
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


#파일 구조 변경시 수정 필요
ENV_PATH = Path(__file__).resolve().parents[1] / "atlas-credentials.env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        #env에 선언 안된 값 존재시 무시
        extra="ignore",
    )

    mongodb_uri: SecretStr = Field(validation_alias="MONGODB_URI")
    mongodb_name: str = Field(validation_alias="MONGODB_NAME")

    app_name: str = "Crawler API"


@lru_cache
def get_settings() -> Settings:
    return Settings()
