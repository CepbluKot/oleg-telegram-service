from bot_modules.forms.data_structures import SentForm
from bot_modules.user_interface.data_structures import (
    CompletingFormDispatcher,
    UserInterface,
)
from bot_modules.user_interface.ui_repository.ui_repository_interface import (
    CompletingFormsDispatcherInterface,
    SelectedUIRepositoryInterface,
)


class CompletingFormsDispatcherAbstraction(CompletingFormsDispatcherInterface):
    def __init__(self, interface: CompletingFormsDispatcherInterface) -> None:
        self.interface = interface

    def add_user(self, user_id: int, sent_form: SentForm):
        return self.interface.add_user(user_id=user_id, sent_form=sent_form)

    def set_next_question(self, user_id: int):
        return self.interface.set_next_question(user_id=user_id)

    def set_current_question_message_id(self, user_id: int, message_id: str):
        return self.interface.set_current_question_message_id(
            user_id=user_id, message_id=message_id
        )

    def get_dispatcher_data(self, user_id: int) -> CompletingFormDispatcher:
        return self.interface.get_dispatcher_data(user_id=user_id)

    def check_is_user_completing_form(self, user_id: int):
        return self.interface.check_is_user_completing_form(user_id=user_id)

    def update_question_answer(
        self, user_id: str, question_message_id: str, new_answer: str
    ):
        return self.interface.update_question_answer(
            user_id=user_id,
            question_message_id=question_message_id,
            new_answer=new_answer,
        )

    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)


class SelectedUIRepositoryAbstraction(SelectedUIRepositoryInterface):
    def __init__(self, interface: SelectedUIRepositoryInterface) -> None:
        self.interface = interface

    def set_users_ui_to_gui(self, user_id: str):
        return self.interface.set_users_ui_to_gui(user_id=user_id)

    def set_users_ui_to_text(self, user_id: str):
        return self.interface.set_users_ui_to_text(user_id=user_id)

    def get_users_ui(self, user_id: str) -> UserInterface:
        return self.interface.get_users_ui(user_id=user_id)

    def check_is_user_selected_ui(self, user_id: str) -> bool:
        return self.interface.check_is_user_selected_ui(user_id=user_id)
