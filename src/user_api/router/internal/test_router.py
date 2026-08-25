from fastapi import Depends

from src.user_api.router import BaseRouter
from src.user_api.service.internal import TestService, get_test_service


class TestRouter(BaseRouter):
    def __init__(self):
        super().__init__(
            prefix = "/test",
            tags = ["internal"],
            response = {403: {"description": "개발 환경에서만 사용 가능"}},
        )

    def setup_routes(self):
        @self.post("/reset-db")
        async def reset_db(service: TestService = Depends(get_test_service)):
            await service.reset_all()
            return {"message": "DB가 초기화되었습니다."}

        @self.post("/drop-db")
        async def drop_db(service: TestService = Depends(get_test_service)):
            await service.drop_all()
            return {"message": "모든 테이블이 삭제되었습니다."}

        @self.post("/setup-test-data")
        async def setup_test_data(service: TestService = Depends(get_test_service)):
            await service.seed_all()
            return {"message": "모든 테스트 데이터의 생성이 완료되었습니다."}