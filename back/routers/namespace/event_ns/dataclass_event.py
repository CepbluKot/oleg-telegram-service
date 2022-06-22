from pydantic import BaseModel, validator, conint, constr, root_validator
from typing import Optional, List, TypedDict, Dict

from datetime import date, time, datetime


class ServiceEvent(BaseModel, total=False):
    """Словарь услуги для события"""
    name_service: str
    quantity: conint(gt=1)


class GroupServiceEvent(BaseModel):
    """Словарь группы услуг"""
    group_event_service: Dict[ServiceEvent]


class NewEvent(BaseModel):
    name: constr(min_length=2, max_length=100)
    day: date
    start_event: time
    end_event: time
    service_this_day: Optional[GroupServiceEvent]

    @root_validator(allow_reuse=True)
    def check_reliability_date(cls, values):
        if ('start_event' not in values) or ('end_event' not in values):
            raise ValueError('error typing time')

        start, end = values.get('start_event'), values.get('end_event')

        if start >= end:
            raise ValueError('start event value less than end event value')
        return values

    @validator('day', pre=True)
    def check_reliability_date(cls, v,  values, **kwargs):
        now_date = datetime.now()
        if 'day' not in values or v > date(year=now_date.year, month=now_date.month, day=now_date.day):
            raise ValueError('dates well, does it exist or is it not valid')
        return v