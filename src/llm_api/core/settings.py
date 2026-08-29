from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from functools import lru_cache
from urllib.parse import quote_plus

#.env 파일 경로
ENV_PATH = Path(__file__).resolve().parents[2] /"llm.env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ENV_PATH, #파일 위치
        env_file_encoding = "utf-8", #읽을 때 인코딩 방식
        extra = "ignore" #모르는 키 있을 때 무시
    )
    nvidia_api_key: SecretStr
    crawler_api_url: str
    user_api_url: str
    db_echo: bool
    log_level: str

    #오라클 접속 정보
    oracle_id: str
    oracle_pw: SecretStr
    oracle_ip: str
    oracle_port: int
    oracle_pdb_name: str

    #오라클 url 조립부
    @property
    def database_url(self) -> str:
        password = quote_plus(self.oracle_pw.get_secret_value())
        return f"oracle+oracledb_async://{self.oracle_id}:{password}"f"@{self.oracle_ip}:{self.oracle_port}/?service_name={self.oracle_pdb_name}"

@lru_cache
def get_settings() -> Settings:
    return Settings()