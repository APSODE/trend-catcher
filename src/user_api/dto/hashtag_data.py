from pydantic import BaseModel, ConfigDict

from src.user_api.decorator import bind_model
from src.user_api.model import HashtagModel


@bind_model(HashtagModel)
class HashtagData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    name: str
