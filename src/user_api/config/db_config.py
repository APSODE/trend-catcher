from pydantic import Field

from src.user_api.config.base_config import BaseConfig


class DatabaseConfig(BaseConfig):
    oracle_id: str = Field(validation_alias = "ORACLE_DB_ID")
    oracle_pw: str = Field(validation_alias = "ORACLE_DB_PW")

    oracle_ip: str = Field(validation_alias = "ORACLE_DB_IP")
    oracle_port: str = Field(validation_alias = "ORACLE_DB_PORT")
    oracle_pdb_name: str = Field(validation_alias = "ORACLE_DB_PDB_NAME")

    redis_pw: str = Field(validation_alias = "REDIS_DB_PW")
    redis_ip: str = Field(validation_alias = "REDIS_DB_IP")
    redis_port: str = Field(validation_alias = "REDIS_DB_PORT")
