from typing import List

from src.user_api.dto import LocalAccountData
from src.user_api.dto.serializer import serialize_many, serialize
from src.user_api.exceptions.account_exceptions import UnknownAccountData
from src.user_api.repository import LocalAccountRepository
from src.user_api.service import BaseService


class AccountService(BaseService):
    def __init__(self, account_repository: LocalAccountRepository):
        self.__account_repository = account_repository

    async def query_all_account(self) -> List[LocalAccountData]:
        account_models = await self.__account_repository.find_all()
        return serialize_many(account_models, LocalAccountData)

    async def query_by_login_id(self, login_id: str) -> LocalAccountData:
        maybe_account_model = await self.__account_repository.get_account_by_login_id(
            login_id = login_id
        )

        if maybe_account_model is None:
            raise UnknownAccountData()

        return serialize(maybe_account_model, LocalAccountData)

    async def query_by_pk(self, pk: int) -> LocalAccountData:
        maybe_account_model = await self.__account_repository.get_account_by_pk(
            account_pk = pk
        )

        if maybe_account_model is None:
            raise UnknownAccountData()

        return serialize(maybe_account_model, LocalAccountData)

    async def query_by_user_pk(self, user_pk: int) -> List[LocalAccountData]:
        maybe_account_models = await self.__account_repository.get_account_by_user_pk(
            user_pk = user_pk
        )

        if maybe_account_models is None:
            raise UnknownAccountData()

        return serialize_many(maybe_account_models, LocalAccountData)



get_account_service = AccountService.create_dependency(
    account_repository = LocalAccountRepository
)


