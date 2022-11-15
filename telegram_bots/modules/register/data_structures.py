from pydantic import BaseModel


class User(BaseModel):
    name: str
    tg_id: int
    phone_num: str
