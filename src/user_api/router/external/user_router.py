from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from src.user_api.auth import get_current_user_pk, get_current_account, bearer_scheme

from src.user_api.dto import (
    LocalRegisterData,
    LocalLoginRequest,
    DeleteRequest,
    RefreshRequest,
    FollowHashtagRequest,
    UnfollowHashtagRequest,
    TokenPair,
    AccountData,
    SocialLoginRequest, SocialRegisterData, SocialLinkRequest
)

from src.user_api.router import BaseRouter

from src.user_api.service.external import(
    UserAccountService,
    get_user_account_service,
    UserHashtagService,
    get_user_hashtag_service
)


class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/user",
            tags = ["external"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.put("/local-register")
        async def local_register(request: LocalRegisterData, service: UserAccountService = Depends(get_user_account_service)):
            await service.local_register(request)
            return {"message": "success"}

        @self.put("/social-register")
        async def social_register(request: SocialRegisterData, service: UserAccountService = Depends(get_user_account_service)):
            await service.social_register(request)
            return {"message": "success"}

        @self.post("/local-login", response_model = TokenPair)
        async def local_login(request: LocalLoginRequest, service: UserAccountService = Depends(get_user_account_service)):
            return await service.local_login(request)


        @self.post("/social-login", response_model = TokenPair)
        async def social_login(request: SocialLoginRequest, service: UserAccountService = Depends(get_user_account_service)):
            return await service.social_login(request)

        @self.post("/social-link")
        async def social_link(request: SocialLinkRequest,
                              user_pk: int = Depends(get_current_user_pk),
                              service: UserAccountService = Depends(get_user_account_service)):
            return await service.link_social_account(user_pk, request)

        @self.post("/logout")
        async def logout(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
                         service: UserAccountService = Depends(get_user_account_service)):
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
                                 account: AccountData = Depends(get_current_account),
                                 service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.follow_hashtag(request, account.user_fk)

        @self.post("/unfollow-hashtag")
        async def unfollow_hashtag(request: UnfollowHashtagRequest,
                                   account: AccountData = Depends(get_current_account),
                                   service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.unfollow_hashtag(request, account.user_fk)
