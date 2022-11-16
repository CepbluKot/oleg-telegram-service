from abc import ABC
from typing import List
from telegram_bots.modules.register.data_structures import User
from telegram_bots.modules.register.repository.repository_interface import RegisterRepositoryInterface


class RegisterRepositoryAbstraction(RegisterRepositoryInterface):
    def __init__(self, interface: RegisterRepositoryInterface) -> None:
        self.interface = interface


    def add_user(self, user: User):
        return self.interface.add_user(user=user)

    
    def get_user(self, tg_id: int) -> User:
        return self.interface.get_user(tg_id=tg_id)

    
    def update_user(self, user: User):
        return self.interface.update_user(user=user)
