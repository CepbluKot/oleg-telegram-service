from pydantic import BaseModel, validator, conint, constr, confloat, root_validator
from typing import Optional, List


class ValidateStaff(BaseModel):
    name_staff: constr(min_length=1)


class FilterStaff(BaseModel):
    id: Optional[List[int]] = None
    name_staff: Optional[List[str]] = None
