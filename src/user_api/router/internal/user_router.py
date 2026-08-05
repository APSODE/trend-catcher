from fastapi import Depends

from src.user_api.dto.request_data import NameQueryRequest, PKQueryRequest
from src.user_api.dto.response_data import DataCollectionResponse
from src.user_api.dto.user_data import UserData
from src.user_api.router.base_router import BaseRouter
from src.user_api.service.internal.user_service import UserService, get_user_service


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