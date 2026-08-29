from src.user_api.dto import DataCollectionResponse, HashtagData
from src.user_api.dto.serializer import serialize_many, required_relation
from src.user_api.repository import UserRepository, UserHashtagRepository, HashtagRepository
from src.user_api.service import BaseService
from src.user_api.model import UserHashtagModel


class UserHashtagService(BaseService):
    def __init__(self,
                 user_repository: UserRepository,
                 hashtag_repository: HashtagRepository,
                 relation_repository: UserHashtagRepository):
        self.__user_repository = user_repository
        self.__hashtag_repository = hashtag_repository
        self.__relation_repository = relation_repository

    async def get_followed_hashtag_list(self) -> DataCollectionResponse[HashtagData]:
        followed_hashtag_list = serialize_many(
            instances = {
                model.hashtag_model
                for model in await self.__relation_repository.find_all(
                    load_relations = [UserHashtagModel.hashtag_model]
                )
            },
            expected_type = HashtagData
        )

        return DataCollectionResponse(
            amount = len(followed_hashtag_list),
            datas = followed_hashtag_list
        )

get_user_hashtag_service = UserHashtagService.create_dependency(
    user_repository = UserRepository,
    hashtag_repository = HashtagRepository,
    relation_repository = UserHashtagRepository
)
