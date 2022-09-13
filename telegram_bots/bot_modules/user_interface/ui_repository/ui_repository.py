from typing import Dict

from bot_modules.forms.data_structures import SentForm
from bot_modules.user_interface.data_structures import (
    CompletingFormDispatcher,
    UserInterface,
)
from bot_modules.user_interface.ui_repository.ui_repository_interface import (
    CompletingFormsDispatcherInterface,
    SelectedUIRepositoryInterface,
)


completing_forms_dispatcher: Dict[str, CompletingFormDispatcher] = {}
user_selected_ui: Dict[str, UserInterface] = {}


class CompletingFormsDispatcher(CompletingFormsDispatcherInterface):
    def add_user(self, user_id: int, sent_form: SentForm):
        user_id = str(user_id)
        dispatcher = CompletingFormDispatcher(
            current_question=sent_form.questions[0],
            current_question_num=0,
            current_sent_form=sent_form,
            answers=[],
            completed_by_user_id=user_id,
        )
        completing_forms_dispatcher[user_id] = dispatcher

    def set_next_question(self, user_id: int):
        user_id = str(user_id)
        completing_forms_dispatcher[user_id].current_question_num += 1
        if not completing_forms_dispatcher[user_id].current_question_num == len(
            completing_forms_dispatcher[user_id].current_sent_form.questions
        ):
            curr_num = completing_forms_dispatcher[user_id].current_question_num
            completing_forms_dispatcher[
                user_id
            ].current_question = completing_forms_dispatcher[
                user_id
            ].current_sent_form.questions[
                curr_num
            ]

    def set_current_question_message_id(self, user_id: int, message_id: str):
        user_id = str(user_id)
        message_id = str(message_id)
        completing_forms_dispatcher[
            user_id
        ].current_question.question_message_id = message_id

    def get_dispatcher_data(self, user_id: int) -> CompletingFormDispatcher:
        user_id = str(user_id)
        if user_id in completing_forms_dispatcher.keys():
            return completing_forms_dispatcher[user_id]

    def check_is_user_completing_form(self, user_id: int):
        user_id = str(user_id)
        return user_id in completing_forms_dispatcher.keys()

    def update_question_answer(
        self, user_id: str, question_message_id: str, new_answer: str
    ):
        for question in completing_forms_dispatcher[
            str(user_id)
        ].current_sent_form.questions:
            print("\n--------\n", question_message_id, question.question_message_id)
            if str(question.question_message_id) == str(int(question_message_id) - 1):

                print("found")
                question.user_answered = str(new_answer)
            print("nfound")

    def delete_user(self, user_id: int):
        user_id = str(user_id)
        completing_forms_dispatcher.pop(user_id, None)


class SelectedUIRepository(SelectedUIRepositoryInterface):
    def set_users_ui_to_gui(self, user_id: str):
        selected_ui = UserInterface(user_id=user_id, GUI=True)
        user_selected_ui[str(user_id)] = selected_ui

    def set_users_ui_to_text(self, user_id: str):
        selected_ui = UserInterface(user_id=user_id, GUI=False)
        user_selected_ui[str(user_id)] = selected_ui

    def get_users_ui(self, user_id: str) -> UserInterface:
        if str(user_id) in user_selected_ui.keys():
            return user_selected_ui[str(user_id)]

    def check_is_user_selected_ui(self, user_id: str) -> bool:
        return str(user_id) in user_selected_ui.keys()
