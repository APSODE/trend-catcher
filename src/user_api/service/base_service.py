from typing import TypeVar
from src.user_api.repository.base_repository import BaseRepository

# T = TypeVar("T", bound = BaseRepository)
# class BaseService:
#     def __init__(self, **repository: T):
#         for repository_name in repository.keys():
#             self.__setattr__(repository_name, repository.keys())

# Service 객체인지 확인하기 위해서만 상속
class BaseService:
    pass
