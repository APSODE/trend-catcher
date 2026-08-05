from pydantic import BaseModel, ConfigDict

from src.user_api.decorator import bind_model
from src.user_api.model import AccountModel


@bind_model(AccountModel)
class AccountData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    user_fk: int
    login_id: str


