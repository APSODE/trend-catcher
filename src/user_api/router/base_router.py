from abc import abstractmethod, ABC
from typing import List, Dict, Any, TypeVar, Generic, Callable, Awaitable

from fastapi import APIRouter

from src.user_api.service.base_service import BaseService

T = TypeVar("T", bound = BaseService)


class BaseRouter(APIRouter, Generic[T], ABC):
    def __init__(
            self,
            prefix: str,
            tags: List[str],
            response: Dict[int, Dict[str, Any]],
            get_service: Callable[..., Awaitable[T]],
    ):
        super().__init__(
            prefix = prefix,
            tags = tags,
            responses = response,
        )

        self._get_service = get_service
        self.setup_routes()

    @abstractmethod
    def setup_routes(self):
        pass