from typing import AsyncGenerator

from fastapi import Depends
from starlette.requests import Request

from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.db.user_account_context import UserAccountContext
from src.user_api.dto.request_data import RegisterRequest, LoginRequest, DeleteRequest
from src.user_api.repository.user_repository import UserRepository
from src.user_api.repository.account_repository import AccountRepository
from src.user_api.router.base_router import BaseRouter
from src.user_api.service.user_account_service import UserAccountService


async def _get_user_account_context() -> AsyncGenerator[UserAccountContext, None]:
    context = UserAccountContext(
        session_factory = DatabaseCreator().session,
        repository_factories = {
            UserRepository: UserRepository,
            AccountRepository: AccountRepository,
        }
    )

    async with context:
        yield context


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
        @self.post("/register")
        async def register(request: RegisterRequest, service: UserAccountService = Depends(self._get_service)):
            await service.register(request)
            return {"message": "success"}

        @self.post("/login")
        async def login(request: LoginRequest, service: UserAccountService = Depends(self._get_service)):
            is_success = await service.login(request)
            return {"success": is_success}

        @self.post("/delete-user")
        async def delete(request: DeleteRequest, service: UserAccountService = Depends(self._get_service)):
            await service.delete(request)