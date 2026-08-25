from src.user_api.dto import PKResponse
from src.user_api.dto.serializer import serialize
from src.user_api.exceptions.user_exceptions import UnknownUserData
from src.user_api.repository import LocalAccountRepository, SocialAccountRepository, UserRepository
from src.user_api.service import BaseService


class UserAccountService(BaseService):
    def __init__(self,
                 local_account_repository: LocalAccountRepository,
                 social_account_repository: SocialAccountRepository,
                 user_repository: UserRepository):
        self.__local_account_repository = local_account_repository
        self.__social_account_repository = social_account_repository
        self.__user_repository = user_repository

    async def get_user_pk_by_provider_user_id(self, provider_user_id: str) -> PKResponse:
        target_user = await self.__social_account_repository.get_account_by_provider_user_id(
            provider_user_id = provider_user_id
        )

        if target_user is None:
            raise UnknownUserData()

        return serialize(target_user, PKResponse)


get_user_account_service = UserAccountService.create_dependency(
    local_account_repository = LocalAccountRepository,
    social_account_repository = SocialAccountRepository,
    user_repository = UserRepository
)