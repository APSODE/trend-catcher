from src.llm_api.repository.base_repository import BaseRepository
from src.llm_api.model.hashtag_model import HashtagModel
from sqlalchemy.ext.asyncio import AsyncSession

class HashtagRepository(BaseRepository[HashtagModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, HashtagModel)

    #해시태그들 매칭
    async def find_by_hashtags(self, hashtags: list[str]) -> list[HashtagModel]:
        if not hashtags:
            return []
        return await self._find_all(HashtagModel.hashtag.in_(hashtags))

    # 모델 포장
    async def create_hashtag(self, hashtag: str, aliases: list[str], children: list[str], embedding: list[float]) ->HashtagModel:
        new_hashtag = HashtagModel(hashtag = hashtag, aliases = aliases, children = children, embedding = embedding)
        return await self.save(new_hashtag)