from typing import List

from src.user_api.constant.permission import Permission
from src.user_api.constant.user_model_constant import MAX_NAME_LENGTH
from src.user_api.exceptions.user_exceptions import InvalidNameException


class UserData:
    def __init__(self, name: str, permission: Permission, interest: List[int]):
        self.__name = name
        self.__permission = permission
        self.__interest = interest

    @staticmethod
    def create_object(name: str, permission: Permission, interest: List[int]):
        return UserData(name, permission, interest)

    @property
    def name(self):
        return self.__name

    @property
    def permission(self):
        return self.__permission

    @property
    def interest(self):
        return self.__interest

    @name.setter
    def name(self, new_name: str):
        if len(new_name) > MAX_NAME_LENGTH:
            raise InvalidNameException(name = new_name, max_length = MAX_NAME_LENGTH)

        else:
            self.__name = new_name

    @permission.setter
    def permission(self, new_permission: Permission):
        self.__permission = new_permission

    def add_interest(self, new_interest: int):
        self.__interest.append(new_interest)




