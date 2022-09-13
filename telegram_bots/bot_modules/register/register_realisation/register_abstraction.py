from typing import List
from bot_modules.register.data_structures import User
from bot_modules.register.register_realisation.register_interface import (
    RegisterForCustomersInterface,
    RegisterForUniversityInterface,
)


class RegisterForUniversutyAbstraction(RegisterForUniversityInterface):
    def __init__(self, interface: RegisterForUniversityInterface) -> None:
        self.interface = interface

    def add_user(self, user: User):
        return self.interface.add_user(user=user)

    def get_all_users_data(self) -> List[User]:
        return self.interface.get_all_users_data()

    def get_user_data(self, user_id: int) -> User:
        return self.interface.get_user_data(user_id=user_id)

    def check_is_user_in_register_data(self, user_id):
        return self.interface.check_is_user_in_register_data(user_id=user_id)

    def update_user_data(self, newUserData: User):
        return self.interface.update_user_data(new_user_data=newUserData)

    def approve_register(self, user_id: int):
        return self.interface.approve_register(user_id=user_id)

    def deny_register(self, user_id: int):
        return self.interface.deny_register(user_id=user_id)

    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)


class RegisterForCustomersAbstraction(RegisterForCustomersInterface):
    def __init__(self, interface: RegisterForCustomersInterface) -> None:
        self.interface = interface

    def add_user(self, user: User):
        return self.interface.add_user(user=user)

    def get_all_users_data(self) -> List[User]:
        return self.interface.get_all_users_data()

    def get_user_data(self, user_id: int) -> User:
        return self.interface.get_user_data(user_id=user_id)

    def check_is_user_in_register_data(self, user_id):
        return self.interface.check_is_user_in_register_data(user_id=user_id)

    def update_user_data(self, newUserData: User):
        return self.interface.update_user_data(new_user_data=newUserData)

    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)
