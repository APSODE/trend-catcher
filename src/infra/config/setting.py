from functools import lru_cache
from typing import Dict, Any, Annotated, Tuple

from pydantic import Field, model_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict, NoDecode
from pathlib import Path


ENV_PATH = Path(__file__).resolve().parents[1] / "url.env"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = str(ENV_PATH),
        env_file_encoding = "utf-8",
        extra = "ignore",
    )

    app_name: str = "Infra API"

    user_api_url: str = Field(validation_alias = "USER_API_URL")
    sns_api_url: str = Field(validation_alias = "SNS_API_URL")
    crawler_api_url: str = Field(validation_alias = "CRAWLER_API_URL")
    llm_api_url: str = Field(validation_alias = "LLM_API_URL")

    frontend_origins: str = Field(validation_alias = "FRONTEND_ORIGINS")

    default_timeout: float = 10.0
    llm_api_timeout: float = 30.0

    jwt_check_path: str = Field(validation_alias = "JWT_CHECK_PATH")

    separator: str = Field(validation_alias = "SEPARATOR")
    protected_url: Annotated[Tuple[str], NoDecode] = Field(validation_alias = "PROTECTED_URL")
    unprotected_url: Annotated[Tuple[str], NoDecode] = Field(validation_alias = "UNPROTECTED_URL")



    @model_validator(mode = "before")
    @classmethod
    def split_url_collection(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        separator = data.get("SEPARATOR")

        for url_collection_key in ["PROTECTED_URL", "UNPROTECTED_URL"]:
            url_collection_str: str = data.get(url_collection_key, "")
            data[url_collection_key] = tuple(url_collection_str.replace("\n", "").strip(separator).split(separator))

        return data

    @computed_field
    @property
    def jwt_check_url(self) -> str:
        return f"{self.user_api_url}{self.jwt_check_path}"


@lru_cache
def get_settings() -> Settings:
    # 정적 타입 체킹으로는 안정성 확인 불가 / 런타임에서 채워지므로 ignore처리
    return Settings() # type: ignore[call-arg]
