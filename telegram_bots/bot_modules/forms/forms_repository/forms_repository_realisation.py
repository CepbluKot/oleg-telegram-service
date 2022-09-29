from typing import Dict, List
from bot_modules.forms.forms_repository.forms_repository_interface import (
    ChoosingGroupsDispatcherInterface,
    CurrentlyEditingFormRepositoryInterface,
    FormsConsturctorRepositoryInterface,
    FormsRepositoryInterface,
    SentFormsRepositoryInterface,
)
from bot_modules.forms.data_structures import (
    ChoosingGroupsDispatcher,
    ChoosingGroupsPoll,
    Form,
    SentForm,
)
from aiogram import types


formsConstructorRepository = {}
forms_repo: List[Form] = []
choosing_groups_repo: Dict[str, ChoosingGroupsDispatcher] = {}
sent_forms: List[SentForm] = []
currently_editing_form: List[str] = []


class FormsConstructorRepositoryRealisation(FormsConsturctorRepositoryInterface):
    """ "Интерфейс хранилища данных о создаваемых формах"""

    def add_form(self, form: Form):
        formsConstructorRepository[str(form.creator.user_id)] = form.copy()

    def get_form(self, user_id: int) -> Form:
        user_id = str(user_id)
        return formsConstructorRepository[user_id].copy()

    def get_form_id(self) -> int:
        return len(formsConstructorRepository)

    def check_is_user_in_repository(self, user_id: int):
        user_id = str(user_id)
        return user_id in formsConstructorRepository.keys()

    def update_form_data(self, form: Form):
        formsConstructorRepository[str(form.creator.user_id)] = form

    def delete_form(self, user_id: int):
        user_id = str(user_id)
        formsConstructorRepository.pop(user_id, None)


class FormsRepositoryRealisation(FormsRepositoryInterface):
    """ "Интерфейс хранилища данных о формах"""

    def add_form(self, form: Form):
        forms_repo.append(form.copy())

    def get_form(self, form_id: str) -> Form:
        form_id = str(form_id)
        for form in forms_repo:
            if str(form.form_id) == form_id:
                return form.copy()

    def get_forms(self, user_id: int) -> List[Form]:
        user_id = str(user_id)
        print(forms_repo)
        search_result = []
        for form in forms_repo:
            if str(form.creator.user_id) == user_id:
                search_result.append(form.copy())
        return search_result.copy()

    def get_all_forms(self) -> List[Form]:
        return forms_repo.copy()

    def generate_form_id(self) -> int:
        return len(forms_repo)

    def update_form_data(self, form: Form):
        for search_form_index in range(len(forms_repo)):
            if str(forms_repo[search_form_index].form_id) == str(form.form_id):
                forms_repo[search_form_index] = form
                return

    def delete_form(self, form_id: str):
        form_id = str(form_id)
        for form in forms_repo:
            if str(form.form_id) == form_id:
                forms_repo.remove(form)
                return


class ChoosingGroupsDispatcherRealisation(ChoosingGroupsDispatcherInterface):
    def add_user(
        self, user_id: int, polls: List[ChoosingGroupsPoll], selected_form: Form
    ):

        dispatcher_data = ChoosingGroupsDispatcher(
            user_id=user_id,
            polls=polls,
            selected_form=selected_form,
            selected_groups=list(),
        )

        choosing_groups_repo[str(user_id)] = dispatcher_data

    def add_selected_groups(self, user_id: int, groups: List[str]):
        user_id = str(user_id)
        choosing_groups_repo[user_id].selected_groups.extend(list(groups))

    def get_user_polls(self, user_id: int) -> List[ChoosingGroupsPoll]:
        user_id = str(user_id)
        return choosing_groups_repo[user_id].polls

    def poll_checker(self, poll_answer: types.PollAnswer):
        if str(poll_answer.user.id) in choosing_groups_repo:
            for poll in choosing_groups_repo[str(poll_answer.user.id)].polls:
                if str(poll.created_by.user_id) == str(poll_answer.user.id):
                    return True

        return False

    def get_selected_groups(self, user_id: int) -> List[str]:
        user_id = str(user_id)
        return choosing_groups_repo[user_id].selected_groups

    def get_selected_form(self, user_id: int) -> Form:
        user_id = str(user_id)
        return choosing_groups_repo[user_id].selected_form

    def is_user_in_list(self, user_id: int):
        user_id = str(user_id)
        return user_id in choosing_groups_repo.keys()

    def remove_user(self, user_id: int):
        user_id = str(user_id)
        choosing_groups_repo.pop(user_id, None)


class SentFormsRepositoryRealisation(SentFormsRepositoryInterface):
    def add_form(self, form: SentForm):
        sent_forms.append(form)

    def generate_sent_form_id(self):
        return len(sent_forms)

    def get_form(self, sent_form_id: str) -> SentForm:
        sent_form_id = str(sent_form_id)
        for form in sent_forms:
            if str(form.sent_form_id) == sent_form_id:
                return form

    def add_completed_user(self, sent_form_id: str, user_id: int):
        sent_form_id = str(sent_form_id)
        user_id = str(user_id)
        for form in sent_forms:
            if str(form.sent_form_id) == sent_form_id:
                form.completed_users_ids.append(user_id)

    def get_forms_sent_by_user(self, user_id: int) -> List[SentForm]:
        user_id = str(user_id)
        search_result = []

        for form in sent_forms:
            if str(form.creator.user_id) == user_id:
                search_result.append(form.copy())

        return search_result

    def get_recieved_forms(self, user_id: int) -> List[SentForm]:
        user_id = str(user_id)
        search_result = []
        for form in sent_forms:
            if user_id in form.sent_to_users_ids:
                search_result.append(form)

        return search_result

    def get_sent_forms(self, user_id: int) -> List[SentForm]:
        user_id = str(user_id)
        search_result = []
        for form in sent_forms:
            if user_id == str(form.creator.user_id):
                search_result.append(form)

        return search_result

    def delete_form(self, sent_form_id: str):
        sent_form_id = str(sent_form_id)
        for form in sent_forms:
            if str(form.sent_form_id) == sent_form_id:
                sent_forms.remove(form)


class CurrentlyEditingFormRepository(CurrentlyEditingFormRepositoryInterface):
    def add_user(self, user_id: int):
        user_id = str(user_id)
        currently_editing_form.append(user_id)

    def check_is_user_in_list(self, user_id: int):
        user_id = str(user_id)
        return user_id in currently_editing_form

    def delete_user(self, user_id: int):
        user_id = str(user_id)
        currently_editing_form.remove(user_id)
