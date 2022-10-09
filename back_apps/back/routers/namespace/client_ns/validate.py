from pydantic import BaseModel, validator, conint, constr, root_validator
from typing import Optional, List

from phonenumbers import (
    NumberParseException,
    PhoneNumberFormat,
    PhoneNumberType,
    format_number,
    is_valid_number,
    number_type,
    parse as parse_phone_number,
)


MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE


class RegisterClient(BaseModel):
    name: Optional[str] = None
    tg_id: int
    phone: Optional[str] = None

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


class FilterClient(BaseModel):
    name: Optional[List[str]] = None
    tg_id: Optional[List[str]] = None
    phone_num: Optional[List[str]] = None