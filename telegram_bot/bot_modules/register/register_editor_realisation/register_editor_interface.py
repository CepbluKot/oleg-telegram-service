from abc import abstractmethod, ABC
from bot_modules.register.data_structures import User, Prepod


class RegisterEditStudentInterface(ABC):
    @abstractmethod
    def set_new_group(self, new_group: str, user_id: int):
        raise NotImplemented

    @abstractmethod
    def set_new_fio(self, new_fio: str, user_id: int):
        raise NotImplemented

    @abstractmethod
    def get_user_data(self, user_id: int) -> User:
        raise NotImplemented

    @abstractmethod
    def approve_register_edit(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def deny_register_edit(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_user_edit(self, user_id: int):
        raise NotImplemented


class RegisterEditPrepodInterface(ABC):
    @abstractmethod
    def set_new_fio(self, new_fio: str, user_id: int):
        raise NotImplemented

    @abstractmethod
    def get_user_data(self, user_id: int) -> Prepod:
        raise NotImplemented

    @abstractmethod
    def approve_register_edit(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def deny_register_edit(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_user_edit(self, user_id: int):
        raise NotImplemented
