from typing import Optional, Sequence

from sqlalchemy.orm import InstrumentedAttribute

from src.user_api.db.db_controller import DatabaseController
from src.user_api.model import UserHashtagModel
from src.user_api.repository.base_repository import BaseRepository


class UserHashtagRepository(BaseRepository[UserHashtagModel]):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(db_controller, UserHashtagModel)

    async def create_relation(self, user_pk: int, hashtag_pk: int, with_flush: bool = False) -> UserHashtagModel:
        new_relation = UserHashtagModel(user_fk = user_pk, hashtag_fk = hashtag_pk)
        await self.add_data(new_relation, with_flush = with_flush)
        return new_relation

    async def delete_relation(self,
                              user_pk: int,
                              hashtag_pk: int,
                              load_relations: Optional[Sequence[InstrumentedAttribute]] = None,
                              with_flush: bool = False) -> None:
        await self.delete(
            filter = (self.model_class.user_fk == user_pk) & (self.model_class.hashtag_fk == hashtag_pk),
            load_relations = load_relations,
            with_flush = with_flush,
        )

    async def is_exist_relation(self,
                                user_pk: int,
                                hashtag_pk: int,
                                load_relations: Optional[Sequence[InstrumentedAttribute]] = None) -> bool:
        return await self.is_exist(
            filter = (self.model_class.user_fk == user_pk) & (self.model_class.hashtag_fk == hashtag_pk),
            load_relations = load_relations
        )

