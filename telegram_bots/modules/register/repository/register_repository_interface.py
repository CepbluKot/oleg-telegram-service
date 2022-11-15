from abc import abstractmethod, ABC
from typing import List
from bot_modules.register.data_structures import User


class RegisterRepositoryInterface(ABC):
    @abstractmethod
    def add_user(self, user: User):
        raise NotImplemented

    @abstractmethod
    def check_is_user_registered(self) -> List[User]:
        raise NotImplemented

    @abstractmethod
    def get_user(self, user_id: int) -> User:
        raise NotImplemented

    @abstractmethod
    def update_user(self, user: User):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented
