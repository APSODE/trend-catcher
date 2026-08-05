from fastapi import Depends

from src.user_api.db.db_creator import DatabaseCreator
from src.user_api.service.base_service import BaseService


class TestService(BaseService):
    def __init__(self, database_creator: DatabaseCreator):
        self.__database_creator = database_creator

    async def drop_all(self) -> None:
        await self.__database_creator.drop_all_table()

    async def reset_all(self) -> None:
        await self.__database_creator.drop_all_table()
        await self.__database_creator.init_db()

async def get_test_service(db_creator: DatabaseCreator = Depends(DatabaseCreator.create_object)) -> TestService:
    return TestService(db_creator)