from typing import List
from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    fio: str
    role: str
    is_register_approved: bool


class Prepod(User):
    role = "prepod"
    related_groups: List[str]


class Student(User):
    role = "student"
    group: str
