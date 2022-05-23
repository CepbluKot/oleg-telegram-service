from pydantic import BaseModel, validator, ValidationError, constr, Json, conint
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
from typing import Optional, Dict


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


class ServiceEvent(BaseModel):
    """Словарь одной услуги"""
    name: str
    items: conint(gt=0)


class GroupServiceEvent(BaseModel):
    """Словарь группы услуг"""
    group_event_service: Dict[ServiceEvent]


class NewEvent(BaseModel):
    name: constr(min_length=2, max_length=100)
    day: date
    start_event: time
    end_event: time
    service_this_day: Optional[GroupServiceEvent]

    @validator('day', pre=True)
    def check_reliability_date(cls, v,  values, **kwargs):
        now_date = datetime.now()
        if 'day' in values and v > date(year=now_date.year, month=now_date.month, day=now_date.day):
            raise ValueError('dates well, does it exist or is it not valid')
        return v

    @validator('start_event', 'end_event')
    def check_reliability_date(cls, start_event: time, end_event: time):
        if start_event > end_event:
            raise ValueError('start event value less than end event value')
        return start_event, end_event




