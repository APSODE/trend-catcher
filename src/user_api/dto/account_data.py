from pydantic import BaseModel


class AccountData(BaseModel):
    login_id: str
    password: str
    salt: str

