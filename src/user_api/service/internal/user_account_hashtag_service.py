from src.user_api.dto import UserSummaryResponse, UserData, AccountData, HashtagData
from src.user_api.dto.serializer import required_relation, serialize_many
from src.user_api.exceptions import UnknownUserData
from src.user_api.repository import LocalAccountRepository, SocialAccountRepository, UserRepository, HashtagRepository
from src.user_api.service import BaseService


class UserAccountHashtagService(BaseService):
    def __init__(self,
                 local_account_repository: LocalAccountRepository,
                 social_account_repository: SocialAccountRepository,
                 hashtag_repository: HashtagRepository,
                 user_repository: UserRepository):
        self.__local_account_repository = local_account_repository
        self.__social_account_repository = social_account_repository
        self.__hashtag_repository = hashtag_repository
        self.__user_repository = user_repository

    async def get_user_by_pk(self, user_pk: int) -> UserSummaryResponse:
        target_user = await self.__user_repository.get_by_pk(
            target_pk = user_pk,
            load_relations = required_relation(UserData)
        )

        if target_user is None:
            raise UnknownUserData()
        hashtag_models = [
            relation.hashtag_model
            for relation in target_user.interest
            if relation.hashtag_model is not None
        ]

        return UserSummaryResponse(
            name = target_user.name,
            local_accounts = serialize_many(target_user.local_accounts, AccountData),
            social_accounts = serialize_many(target_user.social_accounts, AccountData),
            interest = serialize_many(hashtag_models, HashtagData)
        )

get_user_account_hashtag_service = UserAccountHashtagService.create_dependency(
    local_account_repository = LocalAccountRepository,
    social_account_repository = SocialAccountRepository,
    hashtag_repository = HashtagRepository,
    user_repository = UserRepository
)
