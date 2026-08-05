from typing import List

from src.user_api.exceptions.user_exceptions import UnknownUserData
from src.user_api.model import UserModel
from src.user_api.dto.serializer import serialize, serialize_many, required_relation
from src.user_api.dto import UserData
from src.user_api.repository import UserRepository
from src.user_api.service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    async def query_all_user(self) -> List[UserData]:
        user_models = await self.__user_repository.find_all()
        return serialize_many(user_models, UserData)

    async def query_user_by_name(self, user_name: str) -> List[UserData]:
        user_models = await self.__user_repository.get_by_name(user_name)
        return serialize_many(user_models, UserData)

    async def query_user_by_pk(self, user_pk: int) -> UserData:
        user_model = await self.require_exist_user(user_pk)
        return serialize(user_model, UserData)

    async def require_exist_user(self, user_pk) -> UserModel:
        maybe_user_model = await self.__user_repository.get_by_pk(
            target_pk = user_pk
        )

        if maybe_user_model is None:
            raise UnknownUserData()

        return maybe_user_model

get_user_service = UserService.create_dependency(
    user_repository = UserRepository
)



