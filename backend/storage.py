import typing, pydantic


class StorageObject(pydantic.BaseModel):
    text: str
    tg_id: str


storage: typing.List[StorageObject] = []
