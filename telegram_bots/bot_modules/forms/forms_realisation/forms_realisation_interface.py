from abc import ABC, abstractmethod
from typing import List
from bot_modules.forms.data_structures import (
    SentForm,
    Form,
    TextQuestion,
    PollQuestion,
    ChoosingGroupsPoll,
    Question,
)
from aiogram import types


class FormsConstructorInterface(ABC):
    @abstractmethod
    def add_form(self, form: Form):
        raise NotImplemented

    @abstractmethod
    def add_text_question_to_form(self, text_question: TextQuestion, user_id: int):
        raise NotImplemented

    @abstractmethod
    def add_poll_question_to_form(self, poll_question: PollQuestion, user_id: int):
        raise NotImplemented

    @abstractmethod
    def display_form(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def add_form_to_forms_repository(self, form: Form):
        raise NotImplemented

    @abstractmethod
    def generate_form_id(self) -> str:
        raise NotImplemented

    @abstractmethod
    def get_form(self, user_id: int) -> Form:
        raise NotImplemented

    @abstractmethod
    def update_form_data(self, form: Form):
        raise NotImplemented

    @abstractmethod
    def check_is_user_is_creating_form(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_question(self, question_id: str, user_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_form(self, user_id: int):
        raise NotImplemented


class FormsMenuInterface(ABC):
    @abstractmethod
    def add_user_to_choosing_groups_dispatcher(
        self, user_id: int, polls: List[ChoosingGroupsPoll]
    ):
        raise NotImplemented

    @abstractmethod
    def add_selected_groups_to_choosing_groups_dispatcher(
        self, user_id: int, groups: List[str]
    ):
        raise NotImplemented

    @abstractmethod
    def get_user_polls_from_choosing_groups_dispatcher(
        self, user_id: int
    ) -> List[ChoosingGroupsPoll]:
        raise NotImplemented

    @abstractmethod
    def poll_checker_for_choosing_groups_dispatcher(
        self, poll_answer: types.PollAnswer
    ):
        raise NotImplemented

    @abstractmethod
    def get_selected_groups_from_choosing_groups_dispatcher(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def get_selected_form_from_choosing_groups_dispatcher(self, user_id: int) -> Form:
        raise NotImplemented

    @abstractmethod
    def remove_user_from_choosing_groups_dispatcher(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    def send_form(self, form: Form, send_to_groups: List[str]):
        raise NotImplemented

    @abstractmethod
    def send_big_poll(self, user_id: int, poll_options: List[str]) -> List[str]:
        raise NotImplemented

    @abstractmethod
    def get_form_creator_id(self, form_id: str):
        raise NotImplemented

    @abstractmethod
    def get_groups_students_ids(self, groups: List[str]):
        raise NotImplemented


class FormsEditorInterface(ABC):
    @abstractmethod
    async def display_forms_repository(self, user_id: int):
        raise NotImplemented

    @abstractmethod
    async def display_form(self, form_id: str, user_id: int):
        raise NotImplemented

    @abstractmethod
    def set_new_form_name(self, form_id: str, new_name: str):
        raise NotImplemented

    @abstractmethod
    def set_new_question_name(
        self, form_id: int, question_id: int, new_question_name: str
    ):
        raise NotImplemented

    @abstractmethod
    def insert_question(self, form_id: str, insert_after_id: int, question: Question):
        raise NotImplemented

    @abstractmethod
    def edit_poll_options(
        self, form_id: int, question_id: str, new_poll_options: List[str]
    ):
        raise NotImplemented

    @abstractmethod
    def delete_question(self, form_id: int, question_id: int):
        raise NotImplemented

    @abstractmethod
    def delete_form(self, form_id: int):
        raise NotImplemented


class FormsSenderInterface(ABC):
    @abstractmethod
    def get_forms_sent_by_user(self, user_id: int) -> List[SentForm]:
        raise NotImplemented

    @abstractmethod
    def add_sent_form(self, form: SentForm):
        raise NotImplemented

    @abstractmethod
    def add_completed_user(self, sent_form_id: str):
        raise NotImplemented

    @abstractmethod
    def get_accepeted_forms(self, user_id: int) -> List[SentForm]:
        raise NotImplemented

    @abstractmethod
    def get_form(self, sent_form_id: str):
        raise NotImplemented

    @abstractmethod
    def check_is_form_completed(self, sent_form_id: str):
        raise NotImplemented
