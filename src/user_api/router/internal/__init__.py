from typing import List

from src.user_api.router.base_router import BaseRouter
from src.user_api.router.internal.account_router import AccountRouter
from src.user_api.router.internal.test_router import TestRouter
from src.user_api.router.internal.user_account_router import UserAccountRouter
from src.user_api.router.internal.user_router import UserRouter
from src.user_api.router.internal.hashtag_router import HashtagRouter

INTERNAL_ROUTERS: List[BaseRouter] = [
    UserRouter(),
    HashtagRouter(),
    AccountRouter(),
    UserAccountRouter(),
    TestRouter()
]

__all__ = ["INTERNAL_ROUTERS"]