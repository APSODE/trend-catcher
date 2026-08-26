from typing import Annotated

from fastapi import Depends, Query
from src.user_api.constant.account_constant import AccountType, AccountProvider
from src.user_api.dto import DataCollectionResponse, PKQueryRequest, SocialAccountData, CheckTokenRequest, TokenType
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

        @self.get("/get-all-by-type", response_model = DataCollectionResponse)
        async def get_all_accounts_by_account_type(account_type: AccountType,
                                                   service: AccountService = Depends(get_account_service)):
            accounts = await service.query_all_account_by_type(account_type)
            return DataCollectionResponse(
                amount = len(accounts),
                datas = accounts
            )

        @self.get("/get-by-user-pk", response_model = DataCollectionResponse)
        async def get_by_user_pk(request: Annotated[PKQueryRequest, Query()],
                                 service: AccountService = Depends(get_account_service)):
            accounts = await service.query_by_user_pk(request.pk)
            return DataCollectionResponse(
                amount = len(accounts),
                datas = accounts
            )

        @self.get("/get-by-user-pk-and-provider", response_model = SocialAccountData)
        async def get_by_user_pk_and_provider(user_pk: int,
                                              provider: AccountProvider,
                                              service: AccountService = Depends(get_account_service)):
            return await service.query_by_user_pk_and_provider(
                user_pk = user_pk,
                provider = provider
            )

        @self.get("/check-jwt")
        async def check_jwt(request: CheckTokenRequest,
                            service: AccountService = Depends(get_account_service)):
            return await service.check_jwt(request.token, TokenType.ACCESS)
