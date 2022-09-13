from typing import List
from bot_modules.register.register_repository.register_repository_interface import (
    RegisterEditRepositoryInterface,
    RegisterRepositoryInterface,
    CurrentlyChangingRegisterDataRepositoryInterface,
)
from bot_modules.register.data_structures import User


register_data = {}  # userId: stud/prep
edited_register_data = {}  # serId: stud/prep
currently_changing_register_data = []  # userId


class RegisterRepository(RegisterRepositoryInterface):
    def add_user(self, user: User):
        register_data[str(user.user_id)] = user.copy()

    def get_all_users_data(self) -> List[User]:
        return register_data

    def get_user_data(self, user_id: int) -> User:  # problem: int convert to str
        user_id = str(user_id)
        if user_id in register_data.keys():
            return register_data[user_id]

    def check_is_user_in_register_data(self, user_id: int):
        user_id = str(user_id)
        return str(user_id) in register_data.keys()

    def update_user_data(self, user: User):
        register_data[str(user.user_id)] = user.copy()

    def delete_user(self, user_id: int):
        user_id = str(user_id)
        register_data.pop(user_id, None)


class RegisterEditRepository(RegisterEditRepositoryInterface):
    def add_user(self, user: User):
        edited_register_data[str(user.user_id)] = user.copy()

    def get_all_users_data(self) -> List[User]:
        return edited_register_data.copy()

    def get_user_data(self, user_id: int) -> User:
        user_id = str(user_id)
        return edited_register_data[user_id].copy()

    def update_user_data(self, user: User):
        edited_register_data[str(user.user_id)] = user.copy()

    def check_is_user_in_repository(self, user_id: int):
        user_id = str(user_id)
        return user_id in edited_register_data.keys()

    def delete_user(self, user_id: int):
        user_id = str(user_id)
        edited_register_data.pop(user_id, None)


class CurrentlyChangingRegisterDataRepository(
    CurrentlyChangingRegisterDataRepositoryInterface
):
    def add_user(self, user_id: int):
        user_id = str(user_id)
        currently_changing_register_data.append(user_id)

    def check_is_user_in_list(self, user_id: int):
        user_id = str(user_id)
        return user_id in currently_changing_register_data

    def delete_user(self, user_id: int):
        user_id = str(user_id)
        if user_id in currently_changing_register_data:
            currently_changing_register_data.remove(user_id)
