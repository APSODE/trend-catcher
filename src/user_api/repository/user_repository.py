from typing import Optional, Type, List

from src.user_api.constant.permission import Permission
from src.user_api.db.db_controller import DatabaseController
from src.user_api.model.user_model import UserModel
from src.user_api.repository.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db_controller: DatabaseController):
        super().__init__(db_controller, UserModel)


    async def register_user(self,
                            login_id: str,
                            password: str,
                            name: str,
                            permission: int | Permission,
                            interest: Optional[List[int]] = None
                            ):
        await self.add_data(
            UserModel.create_model(login_id, password, name, permission, interest)
        )

    async def update_user_permission(self):

    async def get_by_login_id(self, target_login_id: str) -> Optional[UserModel]:
        return await self.find_one(self.model_class.login_id == target_login_id)

    async def get_by_name(self, target_name: str) -> List[UserModel]:
        return await self.find_all(self.model_class.name == target_name)




