from pydantic import BaseModel, validator, conint, constr, confloat, root_validator
from datetime import time, date

from typing import Optional, List


class ValidateService(BaseModel):
    name_service: constr(min_length=1, max_length=100)
    price: confloat(ge=0)


class FilterServicesStaff(BaseModel):
    name_services: Optional[List]
    name_staff: Optional[List]


class OneConnectSerSt(BaseModel):
    name_services: Optional[str] = None
    name_staff: Optional[str] = None


class AllConnectServiceStaff(BaseModel):
    all_connect: Optional[List[OneConnectSerSt]] = None
