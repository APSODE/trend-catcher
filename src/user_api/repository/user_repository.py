from typing import Optional, List

from src.user_api.constant.permission import Permission
from src.user_api.db.db_controller import DatabaseController
from src.user_api.model.user_model import UserModel
from src.user_api.repository.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(db_controller, UserModel)

    @staticmethod
    def create_repository(db_controller: DatabaseController) -> "UserRepository":
        return UserRepository(db_controller)

    async def create_user(self,
                          name: str,
                          permission: int | Permission,
                          interest: Optional[List[int]] = None,
                          with_flush: bool = False) -> UserModel:
        new_user = UserModel.create_model(name, permission, interest)
        await self.add_data(new_user, with_flush)

        return new_user

    async def update_name(self,
                          user_pk: int,
                          new_name: str,
                          with_flush: bool = False) -> None:
        await self.update_by_pk(
            target_pk = user_pk,
            update_data = {"name": new_name},
            with_flush = with_flush,
        )

    async def update_user_permission(self,
                                     user_pk: int,
                                     new_permission: int | Permission,
                                     with_flush: bool = False) -> None:
        perm_value = new_permission
        if isinstance(new_permission, Permission):
            perm_value = new_permission.value

        await self.update_by_pk(
            target_pk = user_pk,
            update_data = {"permission": perm_value},
            with_flush = with_flush
        )

    async def get_by_name(self, target_name: str) -> List[UserModel]:
        return await self.find_all(self.model_class.name == target_name)


    async def is_exist_pk(self, target_pk: int) -> bool:
        return await self.is_exist(filter = self.model_class.pk == target_pk)






