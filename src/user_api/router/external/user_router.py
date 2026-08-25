from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials
from src.user_api.auth import get_current_user_pk, get_current_account, bearer_scheme

from src.user_api.dto import (
    LocalRegisterRequest,
    LocalLoginRequest,
    DeleteRequest,
    RefreshRequest,
    FollowHashtagRequest,
    UnfollowHashtagRequest,
    TokenPair,
    AccountData,
    SocialLoginRequest, SocialRegisterRequest, SocialLinkRequest, PKQueryRequest, DataCollectionResponse,
    ChangePasswordRequest, SocialUnlinkRequest, UserSummaryResponse
)

from src.user_api.router import BaseRouter

from src.user_api.service.external import (
    UserAccountService,
    get_user_account_service,
    UserHashtagService,
    get_user_hashtag_service, UserAccountHashtagService, get_user_account_hashtag_service
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
        async def local_register(request: LocalRegisterRequest, service: UserAccountService = Depends(get_user_account_service)):
            await service.local_register(request)
            return {"message": "success"}

        @self.put("/social-register")
        async def social_register(request: SocialRegisterRequest, service: UserAccountService = Depends(get_user_account_service)):
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

        @self.patch("/change-password")
        async def update_password(request: ChangePasswordRequest,
                                  current_account = Depends(get_current_account),
                                  service: UserAccountService = Depends(get_user_account_service)):
            await service.change_password(current_account, request.new_password)


        @self.get("/linked-accounts",)
        async def get_linked_account_info(user_pk: int = Depends(get_current_user_pk),
                                          service: UserAccountService = Depends(get_user_account_service)):
            return await service.get_linked_account_info(user_pk)

        @self.delete("/unlink-social-account")
        async def unlink_social_account(request: SocialUnlinkRequest,
                                        user_pk: int = Depends(get_current_user_pk),
                                        service: UserAccountService = Depends(get_user_account_service)):
            await service.unlink_social_account(user_pk, request.provider)

        @self.get("/get-user-summary", response_model = UserSummaryResponse)
        async def get_user_summary(user_pk: int = Depends(get_current_user_pk),
                                   service: UserAccountHashtagService = Depends(get_user_account_hashtag_service)) -> UserSummaryResponse:
            return await service.summary_user_info(user_pk)

        @self.post("/logout")
        async def logout(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
                         service: UserAccountService = Depends(get_user_account_service)):
            await service.logout(credentials.credentials)
            return {"message": "success"}

        @self.delete("/delete-user")
        async def delete(request: DeleteRequest,
                         user_pk: int = Depends(get_current_user_pk),
                         service: UserAccountService = Depends(get_user_account_service)):
            await service.delete_user(user_pk, request)

        @self.post("/refresh", response_model = TokenPair)
        async def refresh(request: RefreshRequest, service: UserAccountService = Depends(get_user_account_service)):
            return await service.refresh_token(request.refresh_token)
