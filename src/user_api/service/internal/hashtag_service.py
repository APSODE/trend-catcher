from typing import List, Optional

from src.user_api.dto.hashtag_data import HashtagData
from src.user_api.exceptions.hashtag_exception import InvalidHashtagAmount
from src.user_api.repository.hashtag_repository import HashtagRepository
from src.user_api.service.base_service import BaseService


class HashtagService(BaseService):
    def __init__(self, hashtag_repository: HashtagRepository):
        self.__hashtag_repository = hashtag_repository

    async def query_all_hashtag(self) -> List[Optional[HashtagData]]:
        await self.__hashtag_repository.find_all(
            filter = None
        )





