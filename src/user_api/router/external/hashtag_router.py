from fastapi import Depends

from src.user_api.auth import get_current_account, get_current_user_pk
from src.user_api.dto import FollowHashtagRequest, AccountData, UnfollowHashtagRequest, DataCollectionResponse
from src.user_api.router import BaseRouter
from src.user_api.service.external import UserHashtagService, get_user_hashtag_service, HashtagService, \
    get_hashtag_service


class HashtagRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/hashtag",
            tags = ["external"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.post("/follow-hashtag")  #
        async def follow_hashtag(request: FollowHashtagRequest,
                                 account: AccountData = Depends(get_current_account),
                                 service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.follow_hashtag(request, account.user_fk)

        @self.post("/unfollow-hashtag")
        async def unfollow_hashtag(request: UnfollowHashtagRequest,
                                   account: AccountData = Depends(get_current_account),
                                   service: UserHashtagService = Depends(get_user_hashtag_service)):
            await service.unfollow_hashtag(request, account.user_fk)

        @self.get("/follow-hashtag-list", response_model = DataCollectionResponse)
        async def get_followed_hashtag_list(user_pk: int = Depends(get_current_user_pk),
                                            service: UserHashtagService = Depends(get_user_hashtag_service)):
            return await service.get_followed_hashtag_list(user_pk)

        @self.get("/hashtag-list", response_model = DataCollectionResponse)
        async def get_hashtag_all_list(service: HashtagService = Depends(get_hashtag_service)):
            return await service.get_all_hashtag_list()


