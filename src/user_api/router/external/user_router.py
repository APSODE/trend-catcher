from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials

from src.user_api.auth.denendencies import get_current_account_pk, bearer_scheme
from src.user_api.dto.request_data import (
    RegisterRequest,
    LoginRequest,
    DeleteRequest,
    RefreshRequest,
    FollowHashtagRequest, UnfollowHashtagRequest
)
from src.user_api.dto.token_data import TokenPair
from src.user_api.router.base_router import BaseRouter
from src.user_api.service.external.user_account_service import UserAccountService, get_user_account_service
from src.user_api.service.external.user_hashtag_service import UserHashtagService, get_user_hashtag_service


class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/user",
            tags = ["dev"],
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

        @self.post("/logout")
        async def logout(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme), service: UserAccountService = Depends(get_user_account_service)):
            await service.logout(credentials.credentials)
            return {"message": "success"}

        @self.delete("/delete-user")
        async def delete(request: DeleteRequest, service: UserAccountService = Depends(get_user_account_service)):
            await service.delete(request)

        @self.post("/refresh", response_model = TokenPair)
        async def refresh(request: RefreshRequest, service: UserAccountService = Depends(get_user_account_service)):
            return await service.refresh_token(request.refresh_token)

        @self.post("/follow-hashtag")
        async def follow_hashtag(request: FollowHashtagRequest,
                                 user_pk: int = Depends(get_current_account_pk),
                                 service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.follow_hashtag(request, user_pk)

        @self.post("/unfollow-hashtag")
        async def unfollow_hashtag(request: UnfollowHashtagRequest,
                                   user_pk: int = Depends(get_current_account_pk),
                                   service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.unfollow_hashtag(request, user_pk)
