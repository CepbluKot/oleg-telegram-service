from pydantic import BaseModel


class User(BaseModel):
    name: str
    tg_id: int
    phone: str
