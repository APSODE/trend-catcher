from fastapi import Depends

from src.user_api.dto.request_data import (
    RegisterRequest,
    LoginRequest,
    DeleteRequest,
    RefreshRequest,
    FollowHashtagRequest, UnfollowHashtagRequest
)
from src.user_api.dto.token_data import TokenPair
from src.user_api.router.base_router import BaseRouter
from src.user_api.service.user_account_service import UserAccountService, get_user_account_service
from src.user_api.service.user_hashtag_service import UserHashtagService, get_user_hashtag_service


class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/user",
            tags = ["dev", "inner-connection-only"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.put("/register")
        async def register(request: RegisterRequest, service: UserAccountService = Depends(get_user_account_service)):
            await service.register(request)
            return {"message": "success"}

        @self.post("/login", response_model = TokenPair)
        async def login(request: LoginRequest, service: UserAccountService = Depends(get_user_account_service)):
            return await service.login(request)

        @self.delete("/delete-user")
        async def delete(request: DeleteRequest, service: UserAccountService = Depends(get_user_account_service)):
            await service.delete(request)

        @self.post("/refresh", response_model = TokenPair)
        async def refresh(request: RefreshRequest, service: UserAccountService = Depends(get_user_account_service)):
            return await service.refresh_token(request.refresh_token)

        @self.post("/follow-hashtag")
        async def follow_hashtag(request: FollowHashtagRequest, service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.follow_hashtag(request)

        @self.post("/unfollow-hashtag")
        async def unfollow_hashtag(request: UnfollowHashtagRequest, service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.unfollow_hashtag(request)
