from pydantic import BaseModel, ConfigDict


class AccountData(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    pk: int
    user_fk: int
    login_id: str


