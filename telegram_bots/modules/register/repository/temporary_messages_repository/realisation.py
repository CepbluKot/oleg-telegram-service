import typing
from aiogram.types import Message


class RegisterTemporaryMessagesRepository:
    def __init__(self) -> None:
        self.repo: typing.Dict[int,typing.List[Message]] = {} # tg_id: list of msgs

    def append(self, data: Message):
        if data.chat.id not in self.repo:
            self.repo[data.chat.id] = []
        self.repo[data.chat.id].append(data)

    def read(self, tg_id: int):
        return self.repo[tg_id]

    def delete(self, tg_id: int):
        self.repo.pop(tg_id, None)
