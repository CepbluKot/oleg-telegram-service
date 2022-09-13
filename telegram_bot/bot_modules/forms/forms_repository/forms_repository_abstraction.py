from typing import List
from bot_modules.forms.forms_repository.forms_repository_interface import (
    ChoosingGroupsDispatcherInterface,
    FormsRepositoryInterface,
    FormsConsturctorRepositoryInterface,
    SentFormsRepositoryInterface,
    CurrentlyEditingFormRepositoryInterface,
)
from bot_modules.forms.data_structures import ChoosingGroupsPoll, Form, SentForm
from aiogram import types


class FormsConstructorRepositoryAbstraction(FormsConsturctorRepositoryInterface):
    """ "Интерфейс хранилища данных о создаваемых формах"""

    def __init__(self, interface: FormsConsturctorRepositoryInterface) -> None:
        self.interface = interface

    def add_form(self, form: Form):
        return self.interface.add_form(form=form)

    def get_form(self, user_id: int) -> Form:
        return self.interface.get_form(user_id=user_id)

    def get_form_id(self) -> int:
        return self.interface.get_form_id()

    def update_form_data(self, form: Form):
        return self.interface.update_form_data(form=form)

    def check_is_user_in_repository(self, user_id: int):
        return self.interface.check_is_user_in_repository(user_id=user_id)

    def delete_form(self, user_id: int):
        return self.interface.delete_form(user_id=user_id)


class FormsRepositoryAbstraction(FormsRepositoryInterface):
    """ "Интерфейс хранилища данных о формах"""

    def __init__(self, interface: FormsRepositoryInterface) -> None:
        self.interface = interface

    def add_form(self, form: Form):
        return self.interface.add_form(form=form)

    def get_form(self, form_id: str) -> Form:
        return self.interface.get_form(form_id=form_id)

    def get_forms(self, user_id: int) -> List[Form]:
        return self.interface.get_forms(user_id=user_id)

    def get_all_forms(self) -> List[Form]:
        return self.interface.get_all_forms()

    def generate_form_id(self) -> int:
        return self.interface.generate_form_id()

    def update_form_data(self, form: Form):
        return self.interface.update_form_data(form=form)

    def delete_form(self, form_id: str):
        return self.interface.delete_form(form_id=form_id)


class ChoosingGroupsDispatcherAbstracction(ChoosingGroupsDispatcherInterface):
    def __init__(self, interface: ChoosingGroupsDispatcherInterface) -> None:
        self.interface = interface

    def add_user(
        self, user_id: int, polls: List[ChoosingGroupsPoll], selected_form: Form
    ):
        return self.interface.add_user(
            user_id=user_id, polls=polls, selected_form=selected_form
        )

    def add_selected_groups(self, user_id: int, groups: List[str]):
        return self.interface.add_selected_groups(user_id=user_id, groups=groups)

    def get_user_polls(self, user_id: int) -> List[ChoosingGroupsPoll]:
        return self.interface.get_user_polls(user_id=user_id)

    def poll_checker(self, poll_answer: types.PollAnswer):
        return self.interface.poll_checker(poll_answer=poll_answer)

    def get_selected_groups(self, user_id: int) -> List[str]:
        return self.interface.get_selected_groups(user_id=user_id)

    def get_selected_form(self, user_id: int) -> Form:
        return self.interface.get_selected_form(user_id=user_id)

    def is_user_in_list(self, user_id: int):
        return self.interface.is_user_in_list(user_id=user_id)

    def remove_user(self, user_id: int):
        return self.interface.remove_user(user_id=user_id)


class SentFormsRepositoryAbstraction(SentFormsRepositoryInterface):
    def __init__(self, interface: SentFormsRepositoryInterface) -> None:
        self.interface = interface

    def add_form(self, form: SentForm):
        return self.interface.add_form(form=form)

    def generate_sent_form_id(self):
        return self.interface.generate_sent_form_id()

    def get_form(self, sent_form_id: str) -> SentForm:
        return self.interface.get_form(sent_form_id=sent_form_id)

    def add_completed_user(self, sent_form_id: str, user_id: int):
        return self.interface.add_completed_user(
            sent_form_id=sent_form_id, user_id=user_id
        )

    def get_forms_sent_by_user(self, user_id: int) -> List[SentForm]:
        return self.interface.get_forms_sent_by_user(user_id=user_id)

    def get_recieved_forms(self, user_id: int) -> List[SentForm]:
        return self.interface.get_recieved_forms(user_id=user_id)

    def get_sent_forms(self, user_id: int) -> List[SentForm]:
        return self.interface.get_sent_forms(user_id=user_id)

    def delete_form(self, sent_form_id: str):
        return self.interface.delete_form(sent_form_id=sent_form_id)


class CurrentlyEditingFormRepositoryAbstraction(
    CurrentlyEditingFormRepositoryInterface
):
    def __init__(self, interface: CurrentlyEditingFormRepositoryInterface) -> None:
        self.interface = interface

    def add_user(self, user_id: int):
        return self.interface.add_user(user_id=user_id)

    def check_is_user_in_list(self, user_id: int):
        return self.interface.check_is_user_in_list(user_id=user_id)

    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)
