from src.user_api.dto.serializer import required_relation, serialize_many
from src.user_api.exceptions import UnknownHashtagData, UnknownUserData, NotFollowedHashtagData, AlreadyFollowedHashtagData
from src.user_api.model import UserModel, HashtagModel
from src.user_api.dto import FollowHashtagRequest, UnfollowHashtagRequest, DataCollectionResponse, HashtagData, UserData
from src.user_api.repository import HashtagRepository, UserHashtagRepository, UserRepository
from src.user_api.service import BaseService


class UserHashtagService(BaseService):
    def __init__(self,
                 user_repository: UserRepository,
                 hashtag_repository: HashtagRepository,
                 relation_repository: UserHashtagRepository):
        self.__user_repository = user_repository
        self.__hashtag_repository = hashtag_repository
        self.__relation_repository = relation_repository


    async def follow_hashtag(self, request: FollowHashtagRequest, user_pk: int):
        target_user = await self.require_exist_user(
            user_pk = user_pk
        )


        hashtag_name = request.target_hashtag.name

        target_hashtag = await self.__hashtag_repository.get_by_tag_name(
            target_name = hashtag_name
        )

        if target_hashtag is None:
            target_hashtag = await self.__hashtag_repository.create_hashtag(
                name = hashtag_name,
                with_flush = True
            )

        else:
            await self.require_not_followed_hashtag(user_pk = user_pk, hashtag_pk = target_hashtag.pk)

        await self.__relation_repository.create_relation(
            user_pk = target_user.pk,
            hashtag_pk = target_hashtag.pk
        )

    async def unfollow_hashtag(self, request: UnfollowHashtagRequest, user_pk: int):
        target_user = await self.require_exist_user(
            user_pk = user_pk
        )

        target_hashtag = await self.require_exist_hashtag(
            hashtag_name = request.target_hashtag.name
        )

        await self.require_already_follow_hashtag(
            user_pk = target_user.pk,
            hashtag_pk = target_hashtag.pk
        )

        await self.__relation_repository.delete_relation(
            user_pk = target_user.pk,
            hashtag_pk = target_hashtag.pk
        )

    async def get_followed_hashtag_list(self, user_pk: int) -> DataCollectionResponse[HashtagData]:
        target_user = await self.__user_repository.get_by_pk(
            target_pk = user_pk,
            load_relations = required_relation(UserData)
        )

        if target_user is None:
            raise UnknownUserData()

        # 기존에는 target_user.interest를 순회하며 매번
        # hashtag_repository.get_by_pk(relation_model.hashtag_fk)로 다시 조회했음(N+1 쿼리).
        # required_relation(UserData)가 이미 relation.hashtag_model까지 로딩해오므로
        # 그대로 재사용하고, orphan 관계(hashtag가 이미 삭제된 경우)는 방어적으로 걸러낸다.
        user_followed_hashtag_models = [
            relation_model.hashtag_model
            for relation_model in target_user.interest
            if relation_model.hashtag_model is not None
        ]

        return DataCollectionResponse(
            amount = len(user_followed_hashtag_models),
            datas = serialize_many(user_followed_hashtag_models, HashtagData)
        )


    async def require_exist_user(self, user_pk: int) -> UserModel:
        maybe_user = await self.__user_repository.get_by_pk(user_pk)
        if maybe_user is None:
            raise UnknownUserData()

        return maybe_user


    async def require_exist_hashtag(self, hashtag_name: str) -> HashtagModel:
        maybe_hashtag = await self.__hashtag_repository.get_by_tag_name(hashtag_name)

        if maybe_hashtag is None:
            raise UnknownHashtagData()

        return maybe_hashtag

    async def require_already_follow_hashtag(self, user_pk: int, hashtag_pk: int):
        if not await self.__relation_repository.is_exist_relation(user_pk = user_pk, hashtag_pk = hashtag_pk):
            raise NotFollowedHashtagData()

    async def require_not_followed_hashtag(self, user_pk: int, hashtag_pk: int):
        if await self.__relation_repository.is_exist_relation(user_pk = user_pk, hashtag_pk = hashtag_pk):
            raise AlreadyFollowedHashtagData()


get_user_hashtag_service = UserHashtagService.create_dependency(
    user_repository = UserRepository,
    hashtag_repository = HashtagRepository,
    relation_repository = UserHashtagRepository
)
