from fastapi import Depends
from src.user_api.dto.hashtag_data import HashtagData
from src.user_api.dto.request_data import NameQueryRequest, PKQueryRequest
from src.user_api.dto.response_data import DataCollectionResponse
from src.user_api.router.base_router import BaseRouter
from src.user_api.service.internal.hashtag_service import HashtagService, get_hashtag_service


class HashtagRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/internal/hashtag",
            tags = ["internal"],
            response = {404: {"description": "Not Found"}}
        )

    def setup_routes(self):
        @self.get("/get-all", response_model = DataCollectionResponse)
        async def get_all_hashtag(service: HashtagService = Depends(get_hashtag_service)):
            hashtags = await service.query_all_hashtag()
            return DataCollectionResponse(
                amount = len(hashtags),
                datas= hashtags
            )

        @self.get("/get-by-name", response_model = HashtagData)
        async def get_hashtag_by_name(request: NameQueryRequest,
                                      service: HashtagService = Depends(get_hashtag_service)):
            return await service.query_hashtag_by_name(request.name)

        @self.get("/get-by-pk", response_model = HashtagData)
        async def get_hashtag_by_pk(request: PKQueryRequest,
                                      service: HashtagService = Depends(get_hashtag_service)):
            return await service.query_hashtag_by_pk(request.pk)


