from typing import List

from src.user_api.router.base_router import BaseRouter
from src.user_api.router.external.user_router import UserRouter

EXTERNAL_ROUTERS: List[BaseRouter] = [
    UserRouter(),
]

__all__ = ["EXTERNAL_ROUTERS"]