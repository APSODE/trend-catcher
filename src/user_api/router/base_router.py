from abc import abstractmethod
from typing import List, Dict, Any

from fastapi import APIRouter
from src.user_api.db.db_controller import DatabaseController


class BaseRouter(APIRouter):
    def __init__(self, prefix: str, tags: List[str], response: Dict[int, Dict[str, Any]], db_controller: DatabaseController):
        super().__init__(
            prefix = prefix,
            tags = tags,
            # dependencies = [Depends(get_token_header)],
            responses = response
        )

        self._db_controller = db_controller
        self.setup_routes()

    @staticmethod
    @abstractmethod
    def create_router(db_controller: DatabaseController):
        pass

    @abstractmethod
    def setup_routes(self):
        pass
