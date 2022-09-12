from typing import List
from bot_modules.register.register_realisation.register_interface import (
    RegisterInterface,
)
from bot_modules.register.data_structures import User
from bot_modules.register.input_output_repositories import register_repository_abs


class RegisterRealisation(RegisterInterface):
    def add_user(self, user: User):
        register_repository_abs.add_user(user=user)

    def get_all_users_data(self) -> List[User]:
        return register_repository_abs.get_all_users_data()

    def get_user_data(self, user_id: int) -> User:
        return register_repository_abs.get_user_data(user_id=user_id)

    def check_is_user_in_register_data(self, user_id):
        return register_repository_abs.check_is_user_in_register_data(user_id=user_id)

    def update_user_data(self, new_user_data: User):
        register_repository_abs.update_user_data(user_data=new_user_data)

    def approve_register(self, user_id: int):
        user_data = register_repository_abs.get_user_data(user_id=user_id)
        user_data.is_register_approved = True
        register_repository_abs.update_user_data(user_data=user_data)

    def deny_register(self, user_id: int):
        register_repository_abs.delete_user(user_id=user_id)

    def delete_user(self, user_id: int):
        register_repository_abs.delete_user(user_id=user_id)
