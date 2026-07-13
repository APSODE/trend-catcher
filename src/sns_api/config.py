"""
SNS 서비스 설정.
환경변수(.env)에서 값을 읽어온다. pydantic-settings 사용.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SNS_", extra="ignore")

    # --- 서비스 기본 ---
    service_name: str = "sns-api"
    debug: bool = False

    # --- Oracle DB ---
    db_url: str = "oracle+oracledb://sns:sns@localhost:1521/?service_name=XEPDB1"
    db_pool_size: int = 5
    db_max_overflow: int = 10
    db_echo: bool = False

    # --- 외부 서비스 (Gateway 뒤에 있는 다른 마이크로서비스) ---
    llm_api_base_url: str = "http://llm-api:8000"       # 개인화/주요 뉴스 생성
    user_api_base_url: str = "http://user-api:8000"     # 유저 정보 조회 (필요 시)

    # --- 발송 채널 ---
    default_discord_webhook_url: str | None = None
    http_timeout_seconds: float = 10.0
    http_max_retries: int = 3

    # --- 내부 트리거 인증 ---
    # 스케줄러/게이트웨이가 /dispatch 를 호출할 때 쓰는 공유 토큰
    internal_token: str = "change-me-in-env"

    # --- 스케줄 (내부 스케줄러를 쓸 경우) ---
    enable_internal_scheduler: bool = False
    morning_cron: str = "0 7 * * *"    # 매일 07:00
    evening_cron: str = "0 19 * * *"   # 매일 19:00
    timezone: str = "Asia/Seoul"


@lru_cache
def get_settings() -> Settings:
    return Settings()