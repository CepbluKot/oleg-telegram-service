from typing import List
from pydantic import BaseModel


class ServiceData(BaseModel):
    day: str
    event: str
    intervals: List[List[str]]
