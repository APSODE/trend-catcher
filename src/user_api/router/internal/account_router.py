from typing import Annotated

from fastapi import Depends, Query

from src.user_api.dto import DataCollectionResponse, LocalAccountData, LoginIDQueryRequest, PKQueryRequest
from src.user_api.router import BaseRouter
from src.user_api.service.internal import AccountService, get_account_service


class AccountRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/internal/account",
            tags = ["internal"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.get("/get-all", response_model = DataCollectionResponse)
        async def get_all_accounts(service: AccountService = Depends(get_account_service)):
            accounts = await service.query_all_account()
            return DataCollectionResponse(
                amount = len(accounts),
                datas = accounts
            )

        @self.get("/get-by-login-id", response_model = LocalAccountData)
        async def get_by_login_id(request: Annotated[LoginIDQueryRequest, Query()],
                                  service: AccountService = Depends(get_account_service)):
            return await service.query_by_login_id(request.login_id)

        @self.get("/get-by-user-pk", response_model = DataCollectionResponse)
        async def get_by_user_pk(request: Annotated[PKQueryRequest, Query()],
                                 service: AccountService = Depends(get_account_service)):
            accounts = await service.query_by_user_pk(request.pk)
            return DataCollectionResponse(
                amount = len(accounts),
                datas = accounts
            )

        @self.get("/get-by-pk", response_model = LocalAccountData)
        async def get_by_pk(request: Annotated[PKQueryRequest, Query()],
                            service: AccountService = Depends(get_account_service)):
            return await service.query_by_pk(request.pk)




