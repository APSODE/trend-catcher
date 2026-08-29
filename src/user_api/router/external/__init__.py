from typing import List

from src.user_api.router.base_router import BaseRouter
from src.user_api.router.external.hashtag_router import HashtagRouter
from src.user_api.router.external.user_router import UserRouter

EXTERNAL_ROUTERS: List[BaseRouter] = [
    UserRouter(),
    HashtagRouter()
]

__all__ = ["EXTERNAL_ROUTERS"]
