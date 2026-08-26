from src.user_api.config.account_config import AccountConfig as _AccountConfig
from src.user_api.config.auth_config import AuthConfig as _AuthConfig
from src.user_api.config.model_config import ModelConfig as _ModelConfig
from src.user_api.config.db_config import DatabaseConfig as _DatabaseConfig

account_config = _AccountConfig.get_config()
auth_config = _AuthConfig.get_config()
model_config = _ModelConfig.get_config()
db_config = _DatabaseConfig.get_config()

__all__ = [
    "account_config",
    "auth_config",
    "model_config",
    "db_config"
]
