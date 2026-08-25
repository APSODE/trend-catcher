from fastapi import Depends

from src.user_api.dto import PKResponse, ProviderUserIDQueryRequest
from src.user_api.router import BaseRouter
from src.user_api.service.internal import get_user_account_service, UserAccountService


class UserAccountRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/internal/user-account",
            tags = ["internal"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.get("/get-pk-by-provider-user-id", response_model = PKResponse)
        async def get_user_pk_by_provider_user_id(request: ProviderUserIDQueryRequest, service: UserAccountService = Depends(get_user_account_service)):
            return service.get_user_pk_by_provider_user_id(request.provider_user_id)