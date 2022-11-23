from abc import ABC
from typing import List
from telegram_bots.modules.register.data_structures import User
from telegram_bots.modules.register.repository.api_repository.repository_interface import (
    RegisterRepositoryInterface,
)


class RegisterRepositoryAbstraction(RegisterRepositoryInterface):
    def __init__(self, interface: RegisterRepositoryInterface) -> None:
        self.interface = interface

    async def get_user(self, tg_id: int) -> User:
        return await self.interface.get_user(tg_id=tg_id)

    async def update_user(self, data: User):
        return await self.interface.update_user(data=data)
