from pydantic import BaseModel


class Data(BaseModel):
    data: BaseModel = BaseModel()
    is_exception: bool = False
    exception_data: dict = ''
