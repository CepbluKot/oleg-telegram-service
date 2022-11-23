from pydantic import BaseModel


class GeneralDataStructure(BaseModel):
    is_exception: bool = False
    exception_data: str = ''
