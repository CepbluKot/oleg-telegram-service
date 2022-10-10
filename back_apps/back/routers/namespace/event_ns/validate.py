from pydantic import BaseModel, validator, conint, constr, root_validator
from typing import Optional, List, TypedDict, Dict

from datetime import date, time, datetime, timedelta


class TimeServices(BaseModel):
    start_time: time
    end_time: time

    @root_validator(allow_reuse=True)
    def check_reliability_date(cls, values):
        if ('start_time' not in values) or ('end_time' not in values):
            raise ValueError('error typing time')

        start, end = values.get('start_time'), values.get('end_time')

        if start >= end:
            raise ValueError('start event value less than end event value')
        return values


class ServiceEvent(BaseModel):
    """Словарь услуги для события"""
    name_service: str
    name_staff: Optional[str] = None
    count_service_this_event: Optional[List[TimeServices]]


class ValidateEvent(BaseModel):
    name: constr(min_length=2, max_length=100)
    day_start: date
    day_end: date
    start_event: time
    end_event: time
    service_this_day: Optional[List[ServiceEvent]]
    weekday_list: Optional[List[int]] = None
    status_repid_day: bool = False
    day_end_repid: Optional[date] = None


    @root_validator(allow_reuse=True)
    def check_reliability_time(cls, values):
        if ('start_event' not in values) or ('end_event' not in values):
            raise ValueError('error typing time')

        if ('day_start' not in values) or ('day_end' not in values):
            raise ValueError('error typing date')

        start_time, end_time = values.get('start_event'), values.get('end_event')
        start_day, end_day = values.get('day_start'), values.get('day_end')

        if start_time >= end_time and start_day >= end_day:
            raise ValueError('start event value less than end event value')

        if end_day - start_day > timedelta(days=1):
            raise ValueError('the difference between days is more than 1')

        if 'day_end_repid' in values:
            day_end_rapid = values.get('day_end_rapid')
            if day_end_rapid and day_end_rapid < start_day:
                raise ValueError('the day was chosen incorrectly')
        return values


class FilterEvent(BaseModel):
    id: Optional[int] = None
    day_start: Optional[date] = None
    day_end: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    name: Optional[List[str]] = None


class WindowDataService(BaseModel):
    start_time: time
    end_time: time
    status_booking: bool
    id_client_booking: int = 0


class UpdateEvent(BaseModel):
    name_field_change_date: List[str]
    id_event: int
    data_service_update: Dict


