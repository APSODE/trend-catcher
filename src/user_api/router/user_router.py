from typing import AsyncGenerator

from fastapi import Depends
from starlette.requests import Request

from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.db.user_account_context import UserAccountContext
from src.user_api.dto.request_data import RegisterRequest, LoginRequest, DeleteRequest, RefreshRequest
from src.user_api.dto.token_data import TokenPair
from src.user_api.repository.user_repository import UserRepository
from src.user_api.repository.account_repository import AccountRepository
from src.user_api.router.base_router import BaseRouter
from src.user_api.service.user_account_service import UserAccountService



async def _get_user_account_service(context: UserAccountContext = Depends(_get_user_account_context)) -> UserAccountService:
    return UserAccountService(
        account_repository = context.accounts,
        user_repository = context.users,
    )


class UserRouter(BaseRouter[UserAccountService]):
    def __init__(self):
        super().__init__(
            prefix = "/user",
            tags = ["dev", "inner-connection-only"],
            response = {404: {"description": "Not Found"}},
            get_service = _get_user_account_service,
        )

    def setup_routes(self):
        @self.put("/register")
        async def register(request: RegisterRequest, service: UserAccountService = Depends(self._get_service)):
            await service.register(request)
            return {"message": "success"}

        @self.post("/login", response_model = TokenPair)
        async def login(request: LoginRequest, service: UserAccountService = Depends(self._get_service)):
            return await service.login(request)

        @self.delete("/delete-user")
        async def delete(request: DeleteRequest, service: UserAccountService = Depends(self._get_service)):
            await service.delete(request)

        @self.post("/refresh", response_model = TokenPair)
        async def refresh(request: RefreshRequest, service: UserAccountService = Depends(self._get_service)):
            return await service.refresh_token(request.refresh_token)