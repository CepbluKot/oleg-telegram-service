from bot_modules.forms.forms_realisation.forms_realisation_interface import (
    FormsConstructorInterface,
    FormsEditorInterface,
    FormsMenuInterface,
    FormsSenderInterface,
)
from bot_modules.forms.data_structures import (
    ChoosingGroupsPoll,
    Form,
    Question,
    SentForm,
    TextQuestion,
    PollQuestion,
)
from typing import List
from aiogram import types


class FormsConstructorAbstracton(FormsConstructorInterface):
    def __init__(self, interface: FormsConstructorInterface) -> None:
        self.interface = interface

    def add_form(self, form: Form):
        return self.interface.add_form(form=form)

    def add_text_question_to_form(self, text_question: TextQuestion, user_id: int):
        return self.interface.add_text_question_to_form(
            text_question=text_question, user_id=user_id
        )

    def add_poll_question_to_form(self, poll_question: PollQuestion, user_id: int):
        return self.interface.add_poll_question_to_form(
            poll_question=poll_question, user_id=user_id
        )

    def display_form(self, user_id: int):
        return self.interface.display_form(user_id=user_id)

    def add_form_to_forms_repository(self, form: Form):
        return self.interface.add_form_to_forms_repository(form=form)

    def generate_form_id(self):
        return self.interface.generate_form_id()

    def get_form(self, user_id: int) -> Form:
        return self.interface.get_form(user_id=user_id)

    def update_form_data(self, form: Form):
        return self.interface.update_form_data(form=form)

    def check_is_user_is_creating_form(self, user_id: int):
        return self.interface.check_is_user_is_creating_form(user_id=user_id)

    def delete_question(self, question_id: str, user_id: int):
        return self.interface.delete_question(question_id=question_id, user_id=user_id)

    def delete_form(self, user_id: int):
        return self.interface.delete_form(user_id=user_id)


# переделать


class FormsMenuAbstraction(FormsMenuInterface):
    def __init__(self, interface: FormsMenuInterface) -> None:
        self.interface = interface

    def add_user_to_choosing_groups_dispatcher(
        self, user_id: int, polls: List[ChoosingGroupsPoll]
    ):
        return self.interface.add_user_to_choosing_groups_dispatcher(
            user_id=user_id, polls=polls
        )

    def add_selected_groups_to_choosing_groups_dispatcher(
        self, user_id: int, groups: List[str]
    ):
        return self.interface.add_selected_groups_to_choosing_groups_dispatcher(
            user_id=user_id, groups=groups
        )

    def get_user_polls_from_choosing_groups_dispatcher(
        self, user_id: int
    ) -> List[ChoosingGroupsPoll]:
        return self.interface.get_user_polls_from_choosing_groups_dispatcher(
            user_id=user_id
        )

    def poll_checker_for_choosing_groups_dispatcher(
        self, poll_answer: types.PollAnswer
    ):
        return self.interface.poll_checker_for_choosing_groups_dispatcher(
            poll_answer=poll_answer
        )

    def get_selected_groups_from_choosing_groups_dispatcher(self, user_id: int):
        return self.interface.get_selected_groups_from_choosing_groups_dispatcher(
            user_id=user_id
        )

    def get_selected_form_from_choosing_groups_dispatcher(self, user_id: int) -> Form:
        return self.interface.get_selected_form_from_choosing_groups_dispatcher(
            user_id=user_id
        )

    def remove_user_from_choosing_groups_dispatcher(self, user_id: int):
        return self.interface.remove_user_from_choosing_groups_dispatcher(
            user_id=user_id
        )

    def send_form(self, form: Form, send_to_groups: List[str]):
        return self.interface.send_form(form=form, send_to_groups=send_to_groups)

    def send_big_poll(self, user_id: int, poll_options: List[str]) -> List[str]:
        return self.interface.send_big_poll(user_id=user_id, poll_options=poll_options)

    def get_form_creator_id(self, form_id: str):
        return self.interface.get_form_creator_id(form_id=form_id)

    def get_groups_students_ids(self, groups: List[str]):
        return self.interface.get_groups_students_ids(groups=groups)


class FormsEditorAbstraction(FormsEditorInterface):
    def __init__(self, interface: FormsEditorInterface) -> None:
        self.interface = interface

    async def display_forms_repository(self, user_id: int):
        return await self.interface.display_forms_repository(user_id=user_id)

    async def display_form(self, form_id: str, user_id: int):
        return await self.interface.display_form(form_id=form_id, user_id=user_id)

    def set_new_form_name(self, form_id: str, new_name: str):
        return self.interface.set_new_form_name(form_id=form_id, new_name=new_name)

    def set_new_question_name(
        self, form_id: int, question_id: int, new_question_name: str
    ):
        return self.interface.set_new_question_name(
            form_id=form_id,
            question_id=question_id,
            new_question_name=new_question_name,
        )

    def insert_question(self, form_id: int, insert_after_id: int, question: Question):
        return self.interface.insert_question(
            form_id=form_id, insert_after_id=insert_after_id, question=question
        )

    def edit_poll_options(
        self, form_id: int, question_id: str, new_poll_options: List[str]
    ):
        return self.interface.edit_poll_options(
            form_id=form_id, question_id=question_id, new_poll_options=new_poll_options
        )

    def delete_question(self, form_id: int, question_id: int):
        return self.interface.delete_question(form_id=form_id, question_id=question_id)

    def delete_form(self, form_id: int):
        return self.interface.delete_form(form_id=form_id)


class FormsSenderAbstraction(FormsSenderInterface):
    def __init__(self, interface: FormsSenderInterface) -> None:
        self.interface = interface

    def get_forms_sent_by_user(self, user_id: int) -> List[SentForm]:
        return self.interface.get_forms_sent_by_user(user_id=user_id)

    def add_sent_form(self, form: SentForm):
        return self.interface.add_sent_form(form=form)

    def add_completed_user(self, sent_form_id: str):
        return self.interface.add_completed_user(sent_form_id=sent_form_id)

    def get_accepeted_forms(self, user_id: int) -> List[SentForm]:
        return self.interface.get_accepeted_forms(user_id=user_id)

    def get_form(self, sent_form_id: str):
        return self.interface.get_form(sent_form_id=sent_form_id)

    def check_is_form_completed(self, sent_form_id: str):
        return self.interface.check_is_form_completed(sent_form_id=sent_form_id)
