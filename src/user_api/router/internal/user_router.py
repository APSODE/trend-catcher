from typing import Annotated

from fastapi import Depends, Query
from src.user_api.dto import NameQueryRequest, PKQueryRequest, DataCollectionResponse, UserData
from src.user_api.router import BaseRouter
from src.user_api.service.internal import UserService, get_user_service


class UserRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/internal/user",
            tags = ["internal"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.get("/get-all", response_model = DataCollectionResponse)
        async def get_all_users(service: UserService = Depends(get_user_service)):
            users = await service.query_all_user()
            return DataCollectionResponse(
                amount = len(users),
                datas = users
            )

        @self.get("/get-by-name", response_model = DataCollectionResponse)
        async def get_users_by_name(request: NameQueryRequest,
                                    service: UserService = Depends(get_user_service)):
            users = await service.query_user_by_name(request.name)
            return DataCollectionResponse(
                amount = len(users),
                datas = users
            )

        @self.get("/get-by-pk", response_model = UserData)
        async def get_user_by_pk(request: PKQueryRequest,
                                 service: UserService = Depends(get_user_service)):
            return await service.query_user_by_pk(request.pk)