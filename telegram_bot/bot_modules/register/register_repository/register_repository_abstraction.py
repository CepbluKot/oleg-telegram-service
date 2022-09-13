from typing import List
from bot_modules.register.register_repository.register_repository_interface import (
    RegisterEditRepositoryInterface,
    RegisterRepositoryInterface,
    CurrentlyChangingRegisterDataRepositoryInterface,
)
from bot_modules.register.data_structures import User


class RegisterRepositoryAbstraction(RegisterRepositoryInterface):
    def __init__(self, interface: RegisterRepositoryInterface) -> None:
        self.interface = interface

    def add_user(self, user: User):
        return self.interface.add_user(user=user)

    def get_all_users_data(self) -> List[User]:
        return self.interface.get_all_users_data()

    def get_user_data(self, user_id: int) -> User:
        return self.interface.get_user_data(user_id=user_id)

    def check_is_user_in_register_data(self, user_id: int):
        return self.interface.check_is_user_in_register_data(user_id=user_id)

    def update_user_data(self, user_data: User):
        return self.interface.update_user_data(user=user_data)

    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)


class RegisterEditRepositoryAbstraction(RegisterEditRepositoryInterface):
    def __init__(self, interface: RegisterEditRepositoryInterface) -> None:
        self.interface = interface

    def add_user(self, user: User):
        return self.interface.add_user(user=user)

    def get_all_users_data(self) -> List[User]:
        return self.interface.get_all_users_data()

    def get_user_data(self, user_id: int) -> User:
        return self.interface.get_user_data(user_id=user_id)

    def update_user_data(self, user: User):
        return self.interface.update_user_data(user=user)

    def check_is_user_in_repository(self, user_id: int):
        return self.interface.check_is_user_in_repository(user_id=user_id)

    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)


class CurrentlyChangingRegisterDataRepositoryAbstraction(
    CurrentlyChangingRegisterDataRepositoryInterface
):
    def __init__(
        self, interface: CurrentlyChangingRegisterDataRepositoryInterface
    ) -> None:
        self.interface = interface

    def add_user(self, user_id: int):
        return self.interface.add_user(user_id=user_id)

    def check_is_user_in_list(self, user_id: int):
        return self.interface.check_is_user_in_list(user_id=user_id)

    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)
