from typing import List, Generic, TypeVar
from pydantic import BaseModel


_DTO = TypeVar("_DTO", bound = BaseModel)

class DataCollectionResponse(BaseModel, Generic[_DTO]):
    amount: int
    datas: List[_DTO]



