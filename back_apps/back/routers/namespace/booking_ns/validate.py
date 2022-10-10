from pydantic import BaseModel, validator, conint, constr, root_validator
from datetime import time, date
import orjson
from typing import Optional, List
from ..service_ns.queries import check_exit_service as verify_exit_service


class BookingValidate(BaseModel):
    time_start: time
    time_end: time
    event_setting_id: conint(ge=1)
    day_start: date
    day_end: date
    service_id: conint(ge=1)
    staff_id: int
    client_id: conint(ge=1)

    @root_validator(allow_reuse=True)
    def check_reliability_date(cls, values):
        if ('time_start' not in values) or ('time_end' not in values) or ('day_end' not in values) or ('day_start' not in values):
            raise ValueError('error typing time')

        time_start, time_end, day_start, day_end = values.get('time_start'), values.get('time_end'), \
                                         values.get('day_start'), values.get('day_end')

        if day_start > day_end:
            raise ValueError('start event value less than end event value')

        if day_start < day_end and time_start < time_end:
            raise ValueError('start event value less than end event value')

        if day_start == day_end and time_start > time_end:
            raise ValueError('start event value less than end event value')
        return values


class AnswerCalendar (BaseModel):
    day: date
    event_day: list


class FilterClientBooking(BaseModel):
    name: Optional[List] = None
    tg_id: Optional[List] = None
    phone_num: Optional[List] = None


class FilterBooking(BaseModel):
    tg_id: Optional[int] = None
    this_date_filter: Optional[date] = None
    date_start_filter: Optional[date] = None
    date_end_filter: Optional[date] = None
    clients_tg_id_filter: Optional[FilterClientBooking] = None
    service_filter: List[str] = None
    time_start_filter: Optional[time] = None
    time_end_filter: Optional[time] = None


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class FreedomBooking(BaseModel):
    day: date
    event: str
    intervals: List[List[time]]

    # class Config:
    #     json_loads = orjson.loads
    #     json_dumps = orjson.loads




