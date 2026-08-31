from src.user_api.dto import DataCollectionResponse, HashtagData, HashtagDataWithFollowerAmount
from src.user_api.dto.serializer import serialize_many, serialize
from src.user_api.repository import HashtagRepository
from src.user_api.service import BaseService
from src.user_api.config import model_config
from src.user_api.exceptions import InvalidHashtagNameLength
from src.user_api.model import HashtagModel


class HashtagService(BaseService):
    def __init__(self, hashtag_repository: HashtagRepository):
        self.__hashtag_repository = hashtag_repository


    async def get_all_hashtag_list(self) -> DataCollectionResponse[HashtagData]:
        hashtag_list = serialize_many(await self.__hashtag_repository.find_all(), HashtagData)

        return DataCollectionResponse(
            amount = len(hashtag_list),
            datas = hashtag_list
        )

    async def add_hashtag(self, hashtag_name: str) -> HashtagData:
        input_hashtag_name_length = len(hashtag_name)
        if input_hashtag_name_length > model_config.HASHTAG_MAX_NAME_LENGTH:
            raise InvalidHashtagNameLength(input_hashtag_name_length, model_config.HASHTAG_MAX_NAME_LENGTH)

        return serialize(await self.__hashtag_repository.create_hashtag(hashtag_name), HashtagData)

    async def get_follower_top_hashtags(self, limit: int = 20) -> DataCollectionResponse[HashtagDataWithFollowerAmount]:
        top_hashtags = await self.__hashtag_repository.find(
            order_by = [HashtagModel.follower_amount.desc()],
            amount = limit
        )

        return DataCollectionResponse(
            amount = len(top_hashtags),
            datas = serialize_many(top_hashtags, HashtagDataWithFollowerAmount)
        )


get_hashtag_service = HashtagService.create_dependency(
    hashtag_repository = HashtagRepository
)
