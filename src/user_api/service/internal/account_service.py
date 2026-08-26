from typing import List, Union

from src.user_api.constant.account_constant import AccountType, AccountProvider
from src.user_api.dto import LocalAccountData, SocialAccountData
from src.user_api.dto.serializer import serialize_many, serialize
from src.user_api.exceptions.account_exceptions import NotExistAccountData
from src.user_api.repository import LocalAccountRepository, SocialAccountRepository
from src.user_api.service import BaseService


class AccountService(BaseService):
    def __init__(self,
                 local_account_repository: LocalAccountRepository,
                 social_account_repository: SocialAccountRepository):
        self.__local_account_repository = local_account_repository
        self.__social_account_repository = social_account_repository

    async def query_all_account(self) -> List[Union[LocalAccountData, SocialAccountData]]:
        local_accounts = await self.__local_account_repository.find_all()
        social_accounts = await self.__social_account_repository.find_all()
        return [
            *serialize_many(social_accounts, SocialAccountData),
            *serialize_many(local_accounts, LocalAccountData)
        ]

    async def query_all_account_by_type(self, account_type: AccountType) -> Union[List[LocalAccountData], List[SocialAccountData]]:
        if account_type == AccountType.LOCAL:
            return serialize_many(
                await self.__local_account_repository.find_all(),
                LocalAccountData
            )
        else:
            return serialize_many(
                await self.__social_account_repository.find_all(),
                SocialAccountData
            )

    async def query_by_user_pk(self, user_pk: int) -> List[Union[LocalAccountData, SocialAccountData]]:
        user_accounts = []

        maybe_local_account = await self.__local_account_repository.get_account_by_user_pk(
            user_pk = user_pk
        )

        if maybe_local_account is not None:
            user_accounts.append(serialize(maybe_local_account, LocalAccountData))

        social_accounts = await self.__social_account_repository.get_accounts_by_user_pk(
            user_pk = user_pk
        )

        if len(social_accounts) > 0:
            user_accounts.extend(serialize_many(social_accounts, SocialAccountData))

        return user_accounts

    async def query_by_user_pk_and_provider(self, user_pk: int, provider: AccountProvider) -> SocialAccountData:
        maybe_social_account = await self.__social_account_repository.get_account_by_user_pk_and_provider(
            user_pk = user_pk,
            provider = provider
        )

        if maybe_social_account is None:
            raise NotExistAccountData()

        return serialize(maybe_social_account, SocialAccountData)


get_account_service = AccountService.create_dependency(
    local_account_repository = LocalAccountRepository,
    social_account_repository = SocialAccountRepository
)
