from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache

#.env 파일 경로
ENV_PATH = Path(__file__).resolve().parents[1] /".env" #테스트돌릴때1 배포에2

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ENV_PATH, #파일 위치
        env_file_encoding = "utf-8", #읽을 때 인코딩 방식
        extra = "ignore" #모르는 키 있을 때 무시
    )
    nvidia_api_key: SecretStr
    database_url: SecretStr
    crawler_api_url: str = "http://100.106.128.75:8081"
    user_api_url: str = "http://100.101.10.83:5175"
    db_echo: bool = False
    log_level: str = "INFO"

@lru_cache
def get_settings() -> Settings:
    return Settings()