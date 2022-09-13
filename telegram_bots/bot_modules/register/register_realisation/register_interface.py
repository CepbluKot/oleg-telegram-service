from abc import abstractmethod, ABC
from typing import List
from bot_modules.register.data_structures import User


class RegisterForUniversityInterface(ABC):
    @abstractmethod
    def add_user(self, user: User):
        raise NotImplemented

    @abstractmethod
    def get_all_users_data(self) -> List[User]:
        raise NotImplemented

    @abstractmethod
    def get_user_data(self, user_id: int) -> User:
        raise NotImplemented

    @abstractmethod
    def check_is_user_in_register_data(self, user_id):
        raise NotImplemented

    @abstractmethod
    def update_user_data(self, new_user_data: User):
        raise NotImplemented

    @abstractmethod
    def approve_register(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def deny_register(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented


class RegisterForCustomersInterface(ABC):
    @abstractmethod
    def add_user(self, user: User):
        raise NotImplemented

    @abstractmethod
    def get_all_users_data(self) -> List[User]:
        raise NotImplemented

    @abstractmethod
    def get_user_data(self, user_id: int) -> User:
        raise NotImplemented

    @abstractmethod
    def check_is_user_in_register_data(self, user_id):
        raise NotImplemented

    @abstractmethod
    def update_user_data(self, new_user_data: User):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented
