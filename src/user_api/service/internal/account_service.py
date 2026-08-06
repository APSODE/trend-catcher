from typing import List

from src.user_api.dto import AccountData
from src.user_api.dto.serializer import serialize_many, serialize
from src.user_api.exceptions.account_exceptions import UnknownAccountData
from src.user_api.repository import AccountRepository
from src.user_api.service import BaseService


class AccountService(BaseService):
    def __init__(self, account_repository: AccountRepository):
        self.__account_repository = account_repository

    async def query_all_account(self) -> List[AccountData]:
        account_models = await self.__account_repository.find_all()
        return serialize_many(account_models, AccountData)

    async def query_by_login_id(self, login_id: str) -> AccountData:
        maybe_account_model = await self.__account_repository.get_account_by_login_id(
            login_id = login_id
        )

        if maybe_account_model is None:
            raise UnknownAccountData()

        return serialize(maybe_account_model, AccountData)

    async def query_by_pk(self, pk: int) -> AccountData:
        maybe_account_model = await self.__account_repository.get_account_by_pk(
            account_pk = pk
        )

        if maybe_account_model is None:
            raise UnknownAccountData()

        return serialize(maybe_account_model, AccountData)

    async def query_by_user_pk(self, user_pk: int) -> List[AccountData]:
        maybe_account_models = await self.__account_repository.get_account_by_user_pk(
            user_pk = user_pk
        )

        if maybe_account_models is None:
            raise UnknownAccountData()

        return serialize_many(maybe_account_models, AccountData)



get_account_service = AccountService.create_dependency(
    account_repository = AccountRepository
)


