from pydantic import BaseModel, constr
from typing import Optional


class ValidateRegister(BaseModel):
    name: constr(min_length=2, max_length=20)
    login: constr(min_length=2, max_length=20)
    password: constr(min_length=7, max_length=100)
    hash_password: Optional[str]


class ValidateLogin(BaseModel):
    login: constr(min_length=2, max_length=20)
    password: constr(min_length=7, max_length=100)