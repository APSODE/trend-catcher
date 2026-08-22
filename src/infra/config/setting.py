from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

#파일 구조 변경시 수정 필요
ENV_PATH = Path(__file__).resolve().parents[1] / "url.env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        #env에 선언 안된 값 존재시 무시
        extra="ignore",
    )

    app_name: str = "Infra API"

    user_api_url : str = Field(validation_alias="USER_API_URL")
    sns_api_url : str = Field(validation_alias="SNS_API_URL")
    crawler_api_url : str = Field(validation_alias="CRAWLER_API_URL")
    llm_api_url : str = Field(validation_alias="LLM_API_URL")

    jwt_secret_key: str = Field(validation_alias="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    redis_url: str = Field(default="redis://redis:6379", validation_alias="REDIS_URL")

    default_timeout : float = 10.0
    llm_api_timeout : float = 30.0

@lru_cache
def get_settings() -> Settings:
    return Settings()

#jwt 검증
#권한
#외부요청 내부요쳥 구분
#api끼리 소통할때는 인증없이 통과할수있도록
#토큰 만료처리는 user에서
