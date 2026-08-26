from src.user_api.dto import UserSummaryResponse, UserData, AccountData, HashtagData
from src.user_api.dto.serializer import required_relation, serialize_many
from src.user_api.exceptions.user_exceptions import UnknownUserData
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

    async def summary_user_info(self, user_pk: int) -> UserSummaryResponse:
        target_user = await self.__user_repository.get_by_pk(
            target_pk = user_pk,
            load_relations = required_relation(UserData)
        )

        if target_user is None:
            raise UnknownUserData()

        # internal/user_account_hashtag_service.py의 get_user_by_pk와 완전히 동일한 로직
        # (N+1 쿼리 제거 + orphan 관계 방어). 두 서비스가 이 로직을 그대로 복제해서
        # 들고 있는 구조 자체가 유지보수 부담이므로, 추후 공통 로직을 베이스 클래스나
        # 공용 함수로 추출하는 것을 권장함(이번 리팩토링 범위에서는 동작 수정에 집중).
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
