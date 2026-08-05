from typing import List

from pydantic import BaseModel

from src.user_api.constant.permission import Permission
from src.user_api.dto.hashtag_data import HashtagData


class RegisterRequest(BaseModel):
    name: str
    permission: int | Permission = Permission.GUEST
    interest: List[int] = []

    login_id: str
    password: str

class LoginRequest(BaseModel):
    login_id: str
    password: str

class LogoutRequest(BaseModel):
    access_token: str

class DeleteRequest(BaseModel):
    login_id: str

class RefreshRequest(BaseModel):
    refresh_token: str

class FollowHashtagRequest(BaseModel):
    target_user_pk: int #TODO JWT에서 USER.PK를 가져올수 있도록 수정하여 payload에 pk를 입력하지 않도록 삭제 해야함
    target_hashtag: HashtagData

class UnfollowHashtagRequest(BaseModel):
    target_user_pk: int #TODO JWT에서 USER.PK를 가져올수 있도록 수정하여 payload에 pk를 입력하지 않도록 삭제 해야함
    target_hashtag: HashtagData

# # ==== 사용..? 안할수도...?
# class CreateHashtagRequest(HashtagData):
#     pass # 이후 필요시 해싱값 추가 예정
#
# class SearchHashtagRequest(BaseModel):
#     target_name: str
#
# class UpdateHashtagRequest(BaseModel):
#     target_name: str
#     new_data: HashtagData
#
# class DeleteHashtagRequest(BaseModel):
#     target_name: str