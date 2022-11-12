from typing import List
from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    fio: str
    role: str


class Prepod(User):
    role = "prepod"
    related_groups: List[str]
    is_register_approved: bool


class Student(User):
    role = "student"
    group: str
    is_register_approved: bool


class SuperCustomer(User):
    role = "customer"
    phone_number: str
    is_register_approved = True
    related_groups = []

class DatabaseUser(BaseModel):
    name_client: str
    tg_id: int
    phone_num: str
    id: int
