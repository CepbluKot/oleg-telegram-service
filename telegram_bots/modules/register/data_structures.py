from pydantic import BaseModel


class User(BaseModel):
    name: str = ''
    tg_id: int = -1
    phone: str = -1


class UserForParse(BaseModel):
    name: str
    tg_id: int
    phone: str
