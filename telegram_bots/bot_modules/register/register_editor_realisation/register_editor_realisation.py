from bot_modules.register.register_editor_realisation.register_editor_interface import (
    RegisterEditStudentInterface,
    RegisterEditPrepodInterface,
)
from bot_modules.register.data_structures import User, Prepod
from bot_modules.register.input_output_repositories import (
    register_edit_repository_abs,
    register_repository_abs,
)


class RegisterEditStudent(RegisterEditStudentInterface):
    def set_new_group(self, new_group: str, user_id: int):
        if not register_edit_repository_abs.check_is_user_in_repository(
            user_id=user_id
        ):
            user_data = register_repository_abs.get_user_data(user_id=user_id)
            register_edit_repository_abs.add_user(user=user_data)

        user_data = register_edit_repository_abs.get_user_data(user_id=user_id)
        user_data.group = new_group
        register_edit_repository_abs.update_user_data(user=user_data)

    def set_new_fio(self, new_fio: str, user_id: int):
        if not register_edit_repository_abs.check_is_user_in_repository(
            user_id=user_id
        ):
            user_data = register_repository_abs.get_user_data(user_id=user_id)
            register_edit_repository_abs.add_user(user=user_data)

        user_data = register_edit_repository_abs.get_user_data(user_id=user_id)
        user_data.fio = new_fio
        register_edit_repository_abs.update_user_data(user=user_data)

    def get_user_data(self, user_id: int) -> User:
        return register_edit_repository_abs.get_user_data(user_id=user_id)

    def approve_register_edit(self, user_id: int):
        userData = register_edit_repository_abs.get_user_data(user_id=user_id)
        register_repository_abs.update_user_data(user_data=userData)
        register_edit_repository_abs.delete_user(user_id=user_id)

    def deny_register_edit(self, user_id: int):
        register_edit_repository_abs.delete_user(user_id=user_id)

    def delete_user_edit(self, user_id: int):
        register_edit_repository_abs.delete_user(user_id=user_id)


class RegisterEditPrepod(RegisterEditPrepodInterface):
    def set_new_fio(self, new_fio: str, user_id: int):
        if not register_edit_repository_abs.check_is_user_in_repository(
            user_id=user_id
        ):
            user_data = register_repository_abs.get_user_data(user_id=user_id)
            register_edit_repository_abs.add_user(user=user_data)

        else:
            user_data = register_edit_repository_abs.get_user_data(user_id=user_id)

        user_data.fio = new_fio
        register_edit_repository_abs.update_user_data(user=user_data)

    def get_user_data(self, user_id: int) -> Prepod:
        return register_edit_repository_abs.get_user_data(user_id=user_id)

    def approve_register_edit(self, user_id: int):
        user_data = register_edit_repository_abs.get_user_data(user_id=user_id)
        register_repository_abs.update_user_data(user=user_data)
        register_edit_repository_abs.delete_user(user_id=user_id)

    def deny_register_edit(self, user_id: int):
        register_edit_repository_abs.delete_user(user_id=user_id)

    def delete_user_edit(self, user_id: int):
        register_edit_repository_abs.delete_user(user_id=user_id)
