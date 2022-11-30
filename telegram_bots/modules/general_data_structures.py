from pydantic import BaseModel
from api.data_structures import ErrorType


class GeneralDataStructure(BaseModel):
    error_data: ErrorType = ErrorType()
