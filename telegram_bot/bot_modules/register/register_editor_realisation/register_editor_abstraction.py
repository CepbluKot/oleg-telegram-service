from bot_modules.register.data_structures import User, Prepod
from bot_modules.register.register_editor_realisation.register_editor_interface import (
    RegisterEditPrepodInterface,
    RegisterEditStudentInterface,
)


class RegisterEditStudentAbstraction(RegisterEditStudentInterface):
    def __init__(self, interface: RegisterEditStudentInterface) -> None:
        self.interface = interface

    def set_new_group(self, new_group: str, user_id: int):
        return self.interface.set_new_group(new_group=new_group, user_id=user_id)

    def set_new_fio(self, new_fio: str, user_id: int):
        return self.interface.set_new_fio(new_fio=new_fio, user_id=user_id)

    def get_user_data(self, user_id: int) -> User:
        return self.interface.get_user_data(user_id=user_id)

    def approve_register_edit(self, user_id: int):
        return self.interface.approve_register_edit(user_id=user_id)

    def deny_register_edit(self, user_id: int):
        return self.interface.deny_register_edit(user_id=user_id)

    def delete_user_edit(self, user_id: int):
        return self.interface.delete_user_edit(user_id=user_id)


class RegisterEditPrepodAbstraction(RegisterEditPrepodInterface):
    def __init__(self, interface: RegisterEditPrepodInterface) -> None:
        self.interface = interface

    def set_new_fio(self, new_fio: str, user_id: int):
        return self.interface.set_new_fio(new_fio=new_fio, user_id=user_id)

    def get_user_data(self, user_id: int) -> Prepod:
        return self.interface.get_user_data(user_id=user_id)

    def approve_register_edit(self, user_id: int):
        return self.interface.approve_register_edit(user_id=user_id)

    def deny_register_edit(self, user_id: int):
        return self.interface.deny_register_edit(user_id=user_id)

    def delete_user_edit(self, user_id: int):
        return self.interface.delete_user_edit(user_id=user_id)
