from abc import abstractmethod, ABC
from typing import List
from telegram_bots.modules.register.data_structures import User


class RegisterRepositoryInterface(ABC):
    @abstractmethod
    async def get_user(self, tg_id: int) -> User:
        raise NotImplemented

    @abstractmethod
    async def update_user(self, data: User):
        raise NotImplemented
