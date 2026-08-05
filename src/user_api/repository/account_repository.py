from typing import Optional, Sequence

from sqlalchemy.orm import InstrumentedAttribute

from src.user_api.db.db_controller import DatabaseController
from src.user_api.model.account_model import AccountModel
from src.user_api.repository.base_repository import BaseRepository
from src.user_api.utils.hash_util import HashedString


class AccountRepository(BaseRepository[AccountModel]):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(db_controller, AccountModel)

    async def create_account(self,
                             user_pk: int,
                             login_id: str,
                             hashed_password: HashedString,
                             personal_salt: str,
                             with_flush: bool = False):
        await self.add_data(
            new_data = AccountModel.create_model(
                user_fk= user_pk,
                login_id = login_id,
                hashed_password = hashed_password,
                personal_salt = personal_salt
            ),
            with_flush = with_flush
        )

    async def get_account_by_pk(self,
                                account_pk: int,
                                load_relations: Optional[Sequence[InstrumentedAttribute]] = None) -> Optional[AccountModel]:
        return await self.find_one(
            filter = self.model_class.pk == account_pk,
            load_relations = load_relations
        )

    async def get_account_by_login_id(self,
                                      login_id: str,
                                      load_relations: Optional[Sequence[InstrumentedAttribute]] = None) -> Optional[AccountModel]:
        return await self.find_one(
            filter = self.model_class.login_id == login_id,
            load_relations = load_relations
        )

    # 반드시 new_password는 hash된 문자열이여야함.
    # 추후 리팩토링 고려
    async def update_password(self, target_account_pk: int, new_password: str, new_salt: str, with_flush: bool = False):
        await self.update_by_pk(
            target_pk = target_account_pk,
            update_data = {"hashed_password": new_password, "personal_salt": new_salt},
            with_flush = with_flush
        )

    async def delete_by_login_id(self,
                                 target_login_id: str,
                                 load_relations: Optional[Sequence[InstrumentedAttribute]] = None):
        await self.delete(
            filter = self.model_class.login_id == target_login_id,
            load_relations = load_relations
        )

    async def is_already_exist_login_id(self,
                                        new_login_id: str,
                                        load_relations: Optional[Sequence[InstrumentedAttribute]] = None) -> bool:
        return await self.is_exist(
            filter = self.model_class.login_id == new_login_id,
            load_relations = load_relations
        )





