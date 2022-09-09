from pydantic import BaseModel, validator, root_validator,constr, conint
from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)
from datetime import date, time, datetime
from typing import Optional, List
from typing_extensions import TypedDict

from queries.queries_services import check_exit_service as verify_exit_service


class RegisterUserConnectA(BaseModel):
    name: constr(min_length=2, max_length=20)
    username: constr(min_length=2, max_length=20)
    password: constr(min_length=7, max_length=100)


MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class RegisterСlient(BaseModel):
    name: constr(min_length=2, max_length=20)
    phone: constr(max_length=30)

    @validator('phone')
    def valid_phone_num(cls, v):
        if v is None:
            return v

        try:
            n = parse_phone_number(v, 'RU')
        except NumberParseException as e:
            raise ValueError('Please provide a valid mobile phone number') from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError('Please provide a valid mobile phone number')

        return format_number(n, PhoneNumberFormat.NATIONAL if n.country_code == 7 else PhoneNumberFormat.INTERNATIONAL)


class ServiceEvent(TypedDict, total=False):
    """Словарь услуги для события"""
    name_service: str
    quantity: conint(gt=1)


class GroupServiceEvent(TypedDict):
    """Словарь группы услуг"""
    group_event_service: ServiceEvent


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





