from redis.asyncio import Redis
from src.user_api.config import db_config

class RedisCreator:
    _single_instance = None

    def __new__(cls):
        if cls._single_instance is None:
            cls._single_instance = super(RedisCreator, cls).__new__(cls)
        return cls._single_instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_RedisCreator__init"):
            cls._RedisCreator__init = True
            self._client = Redis(
                host = db_config.redis_ip,
                port = db_config.redis_port,
                db = 0,
                password = db_config.redis_pw,
                decode_responses = True,
            )

    @property
    def client(self) -> Redis:
        return self._client
