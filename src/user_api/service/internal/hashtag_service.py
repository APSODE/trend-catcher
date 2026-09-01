from typing import List
from src.user_api.exceptions import UnknownHashtagData
from src.user_api.model import HashtagModel
from src.user_api.dto.serializer import serialize, serialize_many
from src.user_api.dto import HashtagData
from src.user_api.repository import HashtagRepository
from src.user_api.service import BaseService


class HashtagService(BaseService):
    def __init__(self, hashtag_repository: HashtagRepository):
        self.__hashtag_repository = hashtag_repository

    async def query_all_hashtag(self) -> List[HashtagData]:
        hashtag_models = await self.__hashtag_repository.find_all()
        return serialize_many(hashtag_models, HashtagData)

    async def query_hashtag_by_name(self, hashtag_name: str) -> HashtagData:
        hashtag_model = await self.require_exist_hashtag_by_name(hashtag_name)
        return serialize(hashtag_model, HashtagData)

    async def query_hashtag_by_pk(self, hashtag_pk: int) -> HashtagData:
        hashtag_model = await self.require_exist_hashtag(hashtag_pk)
        return serialize(hashtag_model, HashtagData)

    async def require_exist_hashtag(self, hashtag_pk: int) -> HashtagModel:
        maybe_hashtag_model = await self.__hashtag_repository.get_by_pk(hashtag_pk)

        if maybe_hashtag_model is None:
            raise UnknownHashtagData()

        return maybe_hashtag_model

    async def require_exist_hashtag_by_name(self, hashtag_name: str) -> HashtagModel:
        maybe_hashtag_model = await self.__hashtag_repository.get_by_tag_name(hashtag_name)

        if maybe_hashtag_model is None:
            raise UnknownHashtagData()

        return maybe_hashtag_model

    async def delete_hashtag(self, hashtag_name: str):
        await self.__hashtag_repository.delete_by_tag_name(
            target_name = hashtag_name,
            with_flush = True
        )

get_hashtag_service = HashtagService.create_dependency(
    hashtag_repository = HashtagRepository
)
