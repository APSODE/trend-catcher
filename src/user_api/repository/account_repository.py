from typing import Optional, Sequence, List

from src.user_api.constant.account_constant import AccountProvider
from src.user_api.db import DatabaseController, RelationPath
from src.user_api.model import LocalAccountModel, SocialAccountModel
from src.user_api.repository.base_repository import BaseRepository
from src.user_api.utils import HashedString


class LocalAccountRepository(BaseRepository[LocalAccountModel]):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(db_controller, LocalAccountModel)

    async def create_account(self,
                             user_pk: int,
                             login_id: str,
                             hashed_password: HashedString,
                             personal_salt: str,
                             with_flush: bool = False) -> LocalAccountModel:
        new_account = LocalAccountModel.create_model(
            user_fk = user_pk,
            login_id = login_id,
            hashed_password = hashed_password,
            personal_salt = personal_salt
        )

        await self.add_data(
            new_data = new_account,
            with_flush = with_flush
        )

        return new_account

    async def get_account_by_login_id(self,
                                      login_id: str,
                                      load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[LocalAccountModel]:
        return await self.find_one(
            filter = self.model_class.login_id == login_id,
            load_relations = load_relations
        )

    async def get_account_by_user_pk(self,
                                     user_pk: int,
                                     load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[LocalAccountModel]:
        return await self.find_one(
            filter = self.model_class.user_fk == user_pk,
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

    async def delete_by_user_pk(self,
                                user_pk: int,
                                load_relations: Optional[Sequence[RelationPath]] = None,
                                with_flush: bool = False):
        await self.delete(
            filter = self.model_class.user_fk == user_pk,
            load_relations = load_relations,
            with_flush = with_flush
        )

    async def delete_by_login_id(self,
                                 target_login_id: str,
                                 load_relations: Optional[Sequence[RelationPath]] = None):
        await self.delete(
            filter = self.model_class.login_id == target_login_id,
            load_relations = load_relations
        )

    async def is_already_exist_login_id(self,
                                        new_login_id: str,
                                        load_relations: Optional[Sequence[RelationPath]] = None) -> bool:
        return await self.is_exist(
            filter = self.model_class.login_id == new_login_id,
            load_relations = load_relations
        )

class SocialAccountRepository(BaseRepository[SocialAccountModel]):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(db_controller, SocialAccountModel)

    async def create_account(self,
                             user_pk: int,
                             provider: AccountProvider,
                             provider_user_id: str,
                             with_flush: bool = False) -> SocialAccountModel:
        new_account = SocialAccountModel.create_model(
            user_fk = user_pk,
            provider = provider,
            provider_user_id = provider_user_id
        )
        await self.add_data(
            new_data = new_account,
            with_flush = with_flush
        )

        return new_account

    async def get_account_by_provider_id(self,
                                         provider: AccountProvider,
                                         provider_user_id: str,
                                         load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[SocialAccountModel]:
        return await self.find_one(
            filter = (self.model_class.provider == provider) & (self.model_class.provider_user_id == provider_user_id),
            load_relations = load_relations
        )

    async def get_accounts_by_provider(self,
                                       provider: AccountProvider,
                                       load_relations: Optional[Sequence[RelationPath]] = None) -> List[SocialAccountModel]:
        return await self.find_all(
            filter = self.model_class.provider == provider,
            load_relations = load_relations
        )

    async def get_account_by_provider_user_id(self,
                                         provider_user_id: str,
                                         load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[SocialAccountModel]:
        return await self.find_one(
            filter = self.model_class.provider_user_id == provider_user_id,
            load_relations = load_relations
        )

    async def get_accounts_by_user_pk(self,
                                      user_pk: int,
                                      load_relations: Optional[Sequence[RelationPath]] = None) -> List[SocialAccountModel]:
        return await self.find_all(
            filter = self.model_class.user_fk == user_pk,
            load_relations = load_relations
        )

    async def get_account_by_user_pk_and_provider(self,
                                                  user_pk: int,
                                                  provider: AccountProvider,
                                                  load_relations: Optional[Sequence[RelationPath]] = None) -> Optional[SocialAccountModel]:
        return await self.find_one(
            filter = (self.model_class.user_fk == user_pk) & (self.model_class.provider == provider),
            load_relations = load_relations
        )

    async def delete_by_user_pk(self,
                                user_pk: int,
                                load_relations: Optional[Sequence[RelationPath]] = None,
                                with_flush: bool = False):
        await self.delete(
            filter = self.model_class.user_fk == user_pk,
            load_relations = load_relations,
            with_flush = with_flush
        )

    async def delete_by_user_pk_and_provider(self,
                                             user_pk: int,
                                             provider: AccountProvider,
                                             load_relations: Optional[Sequence[RelationPath]] = None,
                                             with_flush: bool = False):
        await self.delete(
            filter = (self.model_class.user_fk == user_pk) & (self.model_class.provider == provider),
            load_relations = load_relations,
            with_flush = with_flush
        )

    async def is_already_registered_provider(self,
                                             user_pk: int,
                                             provider: AccountProvider,
                                             load_relations: Optional[Sequence[RelationPath]] = None) -> bool:
        return await self.is_exist(
            filter = (self.model_class.user_fk == user_pk) & (self.model_class.provider == provider),
            load_relations = load_relations
        )
