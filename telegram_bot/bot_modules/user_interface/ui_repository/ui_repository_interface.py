from abc import ABC, abstractmethod
from bot_modules.forms.data_structures import Form, SentForm
from bot_modules.user_interface.data_structures import (
    CompletingFormDispatcher,
    UserInterface,
)


class CompletingFormsDispatcherInterface(ABC):
    @abstractmethod
    def add_user(self, user_id: int, form: Form, sent_form: SentForm):
        raise NotImplemented

    @abstractmethod
    def set_next_question(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def set_current_question_message_id(self, user_id: int, message_id: str):
        raise NotImplemented

    @abstractmethod
    def get_dispatcher_data(self, user_id: int) -> CompletingFormDispatcher:
        raise NotImplemented

    @abstractmethod
    def check_is_user_completing_form(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def update_question_answer(
        self, user_id: str, question_message_id: str, new_answer: str
    ):
        raise NotImplemented

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplemented


class SelectedUIRepositoryInterface(ABC):
    @abstractmethod
    def set_users_ui_to_gui(self, user_id: str):
        raise NotImplemented

    @abstractmethod
    def set_users_ui_to_text(self, user_id: str):
        raise NotImplemented

    @abstractmethod
    def get_users_ui(self, user_id: str) -> UserInterface:
        raise NotImplemented

    @abstractmethod
    def check_is_user_selected_ui(self, user_id: str) -> bool:
        raise NotImplemented
