from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_prefix="SNS_",
        extra="ignore",
    )

    # --- 서비스 기본 ---
    service_name: str = "sns-api"
    debug: bool = False

    # --- Oracle DB ---
    db_url: str = "oracle+oracledb://sns:sns@localhost:1521/?service_name=XEPDB1"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_echo: bool = False

    # --- 외부 서비스 ---
    llm_api_base_url: str = "http://llm-api:8000"
    user_api_base_url: str = "http://user-api:8000"

    # --- 발송 채널 (봇 방식) ---
    discord_bot_token: str = "change-me-in-env"
    major_news_channel_id = "change-me-in-env"
    http_timeout_seconds: float = 10.0
    http_max_retries: int = 3

    # --- 내부 트리거 인증 ---
    internal_token: str = "change-me-in-env"

    # --- 스케줄 ---
    enable_internal_scheduler: bool = False
    morning_cron: str = "0 9 * * *"    # 매일 09:00
    evening_cron: str = "0 21 * * *"   # 매일 21:00
    timezone: str = "Asia/Seoul"


@lru_cache
def get_settings() -> Settings:
    return Settings()