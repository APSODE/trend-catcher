from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

#.env 파일 경로
ENV_PATH = Path(__file__).resolve().parents[2] /".env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ENV_PATH, #파일 위치
        env_file_encoding = "utf-8", #읽을 때 인코딩 방식
        extra = "ignore" #모르는 키 있을 때 무시
    )
    api_key: SecretStr
    db_url: SecretStr
    db_echo = True
    log_level: str = "INFO"

@lru_cache
def get_settings() -> Settings:
    return Settings()