from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot_modules.register.register_handlers.register_handlers_interface import (
    PrepodHandlersInterface,
    StudentHandlersInterface,
)


class PrepodHandlersAbstraction(PrepodHandlersInterface):
    def __init__(self, interface: PrepodHandlersInterface) -> None:
        self.interface = interface

    async def not_confirmed(self, message: types.Message):
        return self.interface.not_confirmed(message=message)

    async def already_registered(self, message: types.Message):
        return self.interface.already_registered(message=message)

    async def ask_register_fio(self, message: types.message, state: FSMContext):
        return self.interface.ask_register_fio(message=message, state=state)

    async def register_fio_chosen(self, message: types.Message, state: FSMContext):
        return self.interface.register_fio_chosen(message=message, state=state)

    async def register_change_true(self, call: types.CallbackQuery, state: FSMContext):
        return self.interface.register_change_false(call=call, state=state)

    async def register_change_false(self, call: types.CallbackQuery, state: FSMContext):
        return self.interface.register_change_false(call=call, state=state)

    async def ask_edited_fio(self, message: types.Message, state: FSMContext):
        return self.interface.ask_edited_fio(message=message, state=state)

    async def set_edited_fio(self, message: types.Message, state: FSMContext):
        return self.interface.set_edited_fio(message=message, state=state)

    async def not_registered(self, message: types.Message):
        return self.interface.not_registered(message=message)

    def prepod_registration_handlers_registrator(self, dp: Dispatcher):
        return self.interface.prepod_registration_handlers_registrator(dp=dp)


class StudentHandlersAbstraction(StudentHandlersInterface):
    def __init__(self, interface: StudentHandlersInterface) -> None:
        self.interface = interface

    async def not_confirmed(self, message: types.Message):
        return self.interface.not_confirmed(message=message)

    async def already_registered(self, message: types.Message, state: FSMContext):
        return self.interface.already_registered(message=message)

    async def ask_register_fio(self, message: types.message, state: FSMContext):
        return self.interface.ask_register_fio(message=message, state=state)

    async def register_fio_chosen(self, message: types.Message, state: FSMContext):
        return self.interface.register_fio_chosen(message=message, state=state)

    async def wrong_group(self, message: types.Message):
        return self.interface.wrong_group(message=message)

    async def register_group_chosen(self, message: types.Message, state: FSMContext):
        return self.interface.register_group_chosen(message=message, state=state)

    async def register_change_true(self, call: types.CallbackQuery, state: FSMContext):
        return self.interface.register_change_true(call=call, state=state)

    async def register_change_false(self, call: types.CallbackQuery, state: FSMContext):
        return self.interface.register_change_false(call=call, state=state)

    async def ask_edited_fio(self, message: types.Message, state: FSMContext):
        return self.interface.ask_edited_fio(message=message, state=state)

    async def set_edited_fio(self, message: types.Message, state: FSMContext):
        return self.interface.set_edited_fio(message=message, state=state)

    async def cancel_handler(self, message: types.Message, state: FSMContext):
        return self.interface.cancel_handler(message=message, state=state)

    async def ask_edited_group(self, message: types.Message, state: FSMContext):
        return self.interface.ask_edited_group(message=message, state=state)

    async def set_edited_group(self, message: types.Message, state: FSMContext):
        return self.interface.set_edited_group(message=message, state=state)

    async def not_registered(self, message: types.Message):
        return self.interface.not_registered(message=message)

    def student_registration_handlers_register(self, dp: Dispatcher):
        return self.interface.student_registration_handlers_register(dp=dp)
