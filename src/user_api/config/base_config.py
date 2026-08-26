from functools import lru_cache
from pathlib import Path
from typing import Optional, Self, cast

from pydantic_settings import SettingsConfigDict, BaseSettings

_DEFAULT_ENV = Path(__file__).resolve().parent / "test.env"

class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = str(),
        env_file_encoding = "utf-8",
        extra = "ignore",
    )

    @classmethod
    def get_config(cls, env_file: Optional[str] = None) -> Self:
        return cast(Self, cls.__get_cached(env_file))

    @classmethod
    @lru_cache
    def __get_cached(cls, env_file: Optional[str] = None) -> "BaseConfig":
        if env_file is None:
            return cls(_env_file = _DEFAULT_ENV)  # type: ignore[call-arg]

        return cls(_env_file = env_file)  # type: ignore[call-arg]