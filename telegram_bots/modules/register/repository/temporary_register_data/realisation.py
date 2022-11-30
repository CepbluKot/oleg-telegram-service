import typing
from telegram_bots.modules.register.data_structures import User


class TemporaryRegisterData:
    def __init__(self) -> None:
        self.repo: typing.Dict[int, User] = {} # tg_id: user

    def create(self, data: User):
        self.repo[data.tg_id] = data

    def read(self, tg_id: int) -> User:
        return self.repo[tg_id]

    def update(self, data: User):
        self.repo[data.tg_id] = data

    def delete(self, tg_id: int):
        self.repo.pop(tg_id, None)
