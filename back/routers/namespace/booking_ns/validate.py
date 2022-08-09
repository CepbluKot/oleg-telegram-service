from pydantic import BaseModel, validator, conint, constr, root_validator
from datetime import time, date

from typing import Optional, List
from routers.namespace.service_ns.queries import check_exit_service as verify_exit_service


class BookingSchema(BaseModel):
    time_start: time
    time_end: time
    id_event: conint(gt=1)
    tg_id: conint(gt=4)
    name_service: constr(min_length=2)

    @root_validator(allow_reuse=True)
    def check_reliability_date(cls, values):
        if ('time_start' not in values) or ('time_end' not in values):
            raise ValueError('error typing time')

        start, end = values.get('time_start'), values.get('time_end')

        if start >= end:
            raise ValueError('start event value less than end event value')
        return values

    @validator('name_service')
    def check_exit_service(cls, v,  values, **kwargs):
        if 'name_service' not in values or not verify_exit_service(v):
            raise ValueError('error typing time')
        return values


class FilterClientBooking(BaseModel):
    name: Optional[List] = None
    tg_id: Optional[List] = None
    phone_num: Optional[List] = None


class FilterBooking(BaseModel):
    this_date_filter: Optional[date] = None
    date_start_filter: Optional[date] = None
    date_end_filter: Optional[date] = None
    clients_tg_id_filter: Optional[FilterClientBooking] = None
    service_filter: List[str] = None
    time_start_filter: Optional[time] = None
    time_end_filter: Optional[time] = None



