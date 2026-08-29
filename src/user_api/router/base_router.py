from abc import abstractmethod, ABC
from typing import List, Dict, Any, TypeVar

from fastapi import APIRouter

from src.user_api.service import BaseService

T = TypeVar("T", bound = BaseService)


class BaseRouter(APIRouter, ABC):
    def __init__(
            self,
            prefix: str,
            tags: List[str],
            response: Dict[int, Dict[str, Any]]
    ):
        super().__init__(
            prefix = prefix,
            tags = tags,
            responses = response,
        )

        self.setup_routes()

    @abstractmethod
    def setup_routes(self):
        pass
