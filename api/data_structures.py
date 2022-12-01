import pydantic


class ErrorType(pydantic.BaseModel):
    has_error: bool = False
    timeout: bool = False
    bad_request: bool = False
    not_found: bool = False
    wrong_phone_number: bool = False
    unauthorized: bool = False
    user_already_exists: bool = False
    booking_doesnt_exist: bool = False
    user_not_found: bool = False

class ApiOutput():
    def __init__(self, data, errors: ErrorType) -> None:
        self.data = data
        self.errors: ErrorType = errors
