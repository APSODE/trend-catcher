from typing import Optional, Sequence
from src.user_api.db import DatabaseController, RelationPath
from src.user_api.model import HashtagModel
from src.user_api.repository.base_repository import BaseRepository


class HashtagRepository(BaseRepository[HashtagModel]):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(db_controller, HashtagModel)

    async def create_hashtag(self, name: str, with_flush: bool = False) -> HashtagModel:
        new_hashtag = HashtagModel(name = name)
        await self.add_data(
            new_data = new_hashtag,
            with_flush = with_flush
        )
        return new_hashtag

    async def get_by_tag_name(self,
                              target_name: str,
                              load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[HashtagModel]:
        return await self.find_one(
            filter = self.model_class.name == target_name,
            load_relations = load_relations
        )

    async def update_tag_name(self, target_name: str, new_name: str, with_flush: bool = False):
        await self.update(
            filter = self.model_class.name == target_name,
            update_data = {"name": new_name},
            with_flush = with_flush
        )

    async def delete_by_tag_name(self,
                                 target_name: str,
                                 with_flush: bool = False,
                                 load_relations: Optional[Sequence[RelationPath]] = None):
        await self.delete(
            filter = self.model_class.name == target_name,
            load_relations = load_relations,
            with_flush = with_flush
        )

    async def is_exist_by_tag_name(self,
                                   target_name: str,
                                   load_relations: Optional[Sequence[RelationPath]] = None) -> bool:
        return await self.is_exist(
            filter = self.model_class.name == target_name,
            load_relations = load_relations
        )

