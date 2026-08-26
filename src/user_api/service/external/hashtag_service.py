from src.user_api.dto import DataCollectionResponse, HashtagData
from src.user_api.dto.serializer import serialize_many
from src.user_api.repository import HashtagRepository
from src.user_api.service import BaseService


class HashtagService(BaseService):
    def __init__(self, hashtag_repository: HashtagRepository):
        self.__hashtag_repository = hashtag_repository


    async def get_all_hashtag_list(self) -> DataCollectionResponse[HashtagData]:
        hashtag_list = serialize_many(await self.__hashtag_repository.find_all(), HashtagData)

        return DataCollectionResponse(
            amount = len(hashtag_list),
            datas = hashtag_list
        )

get_hashtag_service = HashtagService.create_dependency(
    hashtag_repository = HashtagRepository
)
