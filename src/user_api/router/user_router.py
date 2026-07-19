from abc import ABC
from typing import List, Dict

from starlette.requests import Request

from src.user_api.db.db_controller import DatabaseController
from src.user_api.router.base_router import BaseRouter


class UserRouter(BaseRouter):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(
            prefix = "/user",
            tags = ["dev", "inner-connection-only"],
            response = {404: {"description": "Not Found"}},
            db_controller = db_controller
        )

    @staticmethod
    def create_router(db_controller: DatabaseController):
        return UserRouter(db_controller = db_controller)

    def setup_routes(self):
        @self.get("/login")
        async def login(request: Request):
            pass

        @self.get("/register")
        async def register(request: Request):
            pass

        @self.get("/query-interest-category")
        async def query_interest_category(request: Request):
            pass

        @self.get("/change-permission")
        async def change_permission(request: Request):
            pass
