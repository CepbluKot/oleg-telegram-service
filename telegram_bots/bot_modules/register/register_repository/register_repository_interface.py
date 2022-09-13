from abc import abstractmethod, ABC
from typing import List
from bot_modules.register.data_structures import User


class RegisterRepositoryInterface(ABC):
    """ "Интерфейс хранилища данных о студентах"""

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
    def check_is_user_in_register_data(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def update_user_data(self, user: User):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented


class RegisterEditRepositoryInterface(ABC):
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
    def update_user_data(self, user: User):
        raise NotImplemented

    @abstractmethod
    def check_is_user_in_repository(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented


class CurrentlyChangingRegisterDataRepositoryInterface(ABC):
    @abstractmethod
    def add_user(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def check_is_user_in_list(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented
