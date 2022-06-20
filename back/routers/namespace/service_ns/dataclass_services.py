from pydantic import BaseModel, validator, conint, constr, root_validator
from datetime import time, date

from typing import Optional, List


class FilterServices(BaseModel):
    name_services: Optional[List] = None
    name_staff: Optional[List] = None
