from abc import abstractmethod, ABC
from typing import List
from bot_modules.forms.data_structures import ChoosingGroupsPoll, Form, SentForm
from bot_modules.register.data_structures import (
    User,
    Prepod,
)
from aiogram import types


class FormsConsturctorRepositoryInterface(ABC):
    """ "Интерфейс хранилища данных о создаваемых формах"""

    @abstractmethod
    def add_form(self, user_id: int, form: Form):
        raise NotImplemented

    @abstractmethod
    def get_form(self, user_id: int) -> Form:
        raise NotImplemented

    @abstractmethod
    def get_form_id(self) -> int:
        raise NotImplemented

    @abstractmethod
    def update_form_data(self, form: Form):
        raise NotImplemented

    @abstractmethod
    def check_is_user_in_repository(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_form(self, user_id: int):
        raise NotImplemented


class FormsRepositoryInterface(ABC):
    """ "Интерфейс хранилища данных о формах"""

    @abstractmethod
    def add_form(self, form: Form):
        raise NotImplemented

    @abstractmethod
    def get_form(self, form_id: str) -> Form:
        raise NotImplemented

    @abstractmethod
    def get_forms(self, user_id: int) -> Form:
        raise NotImplemented

    def get_all_forms(self) -> List[Form]:
        pass

    @abstractmethod
    def generate_form_id(self) -> int:
        raise NotImplemented

    @abstractmethod
    def update_form_data(self, form: Form):
        raise NotImplemented

    @abstractmethod
    def delete_form(self, form_id: str):
        raise NotImplemented


class PrepodRegisterRepositoryInterface(ABC):
    """ "Интерфейс хранилища данных о преподавателях"""

    @abstractmethod
    def create(self):
        raise NotImplemented

    @abstractmethod
    def read(self):
        raise NotImplemented

    @abstractmethod
    def update(self):
        raise NotImplemented

    @abstractmethod
    def delete(self):
        raise NotImplemented


class ChoosingGroupsDispatcherInterface(ABC):
    @abstractmethod
    def add_user(
        self, user_id: int, polls: List[ChoosingGroupsPoll], selected_form: Form
    ):
        raise NotImplemented

    @abstractmethod
    def add_selected_groups(self, user_id: int, groups: List[str]):
        raise NotImplemented

    @abstractmethod
    def get_user_polls(self, user_id: int) -> List[ChoosingGroupsPoll]:
        raise NotImplemented

    @abstractmethod
    def poll_checker(self, poll_answer: types.PollAnswer):
        raise NotImplemented

    @abstractmethod
    def get_selected_groups(self, user_id: int) -> List[str]:
        raise NotImplemented

    @abstractmethod
    def get_selected_form(self, user_id: int) -> Form:
        raise NotImplemented

    @abstractmethod
    def is_user_in_list(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def remove_user(self, user_id: int):
        raise NotImplemented


class SentFormsRepositoryInterface(ABC):
    @abstractmethod
    def add_form(self, form: SentForm):
        raise NotImplemented

    @abstractmethod
    def generate_sent_form_id(self):
        raise NotImplemented

    @abstractmethod
    def get_form(self, sent_form_id: str) -> SentForm:
        raise NotImplemented

    @abstractmethod
    def add_completed_user(self, sent_form_id: str, user_id: int):
        raise NotImplemented

    @abstractmethod
    def get_forms_sent_by_user(self, user_id: int) -> List[SentForm]:
        raise NotImplemented

    @abstractmethod
    def get_recieved_forms(self, user_id: int) -> List[SentForm]:
        raise NotImplemented

    @abstractmethod
    def get_sent_forms(self, user_id: int) -> List[SentForm]:
        raise NotImplemented

    @abstractmethod
    def delete_form(self, sent_form_id: str):
        raise NotImplemented


class CurrentlyEditingFormRepositoryInterface(ABC):
    @abstractmethod
    def add_user(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def check_is_user_in_list(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented
