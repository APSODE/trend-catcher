from typing import List, Generic, TypeVar, Optional
from pydantic import BaseModel

from src.user_api.constant.account_constant import AccountProvider
from src.user_api.decorator import bind_model
from src.user_api.model import UserModel

_DTO = TypeVar("_DTO", bound = BaseModel)

class DataCollectionResponse(BaseModel, Generic[_DTO]):
    amount: int
    datas: List[_DTO]

@bind_model(UserModel)
class PKResponse(BaseModel):
    pk: int

class OAuth2Response(BaseModel):
    name: Optional[str] = None
    provider: AccountProvider
    provider_user_id: str



