from fastapi import Depends

from src.user_api.router import BaseRouter
from src.user_api.service.internal import UserHashtagService, get_user_hashtag_service
from src.user_api.dto import DataCollectionResponse, HashtagData


class UserHashtagRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/internal/user-hashtag",
            tags = ["internal"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.get("/get-followed-hashtags", response_model = DataCollectionResponse[HashtagData])
        async def get_followed_hashtag_list(service: UserHashtagService = Depends(get_user_hashtag_service)):
            return await service.get_followed_hashtag_list()



