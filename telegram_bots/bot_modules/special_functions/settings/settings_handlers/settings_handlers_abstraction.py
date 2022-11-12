from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot_modules.settings.settings_handlers.settings_handlers_interface import (
    SpecialSettingsHandlersInterface,
)

from bot_modules.special_functions.settings.input_output_repositories import (
    settings_repository_abs,
)


class SettingsHandlersAbstraction(SpecialSettingsHandlersInterface):
    def __init__(self, interface: SpecialSettingsHandlersInterface) -> None:
        self.interface = interface

    async def show_setting_menu(self, message: types.Message):
        return self.interface.show_setting_menu(message=message)

    async def edit_setting_menu(
        self, message: types.Message, call: types.CallbackQuery
    ):
        return self.interface.edit_setting_menu(message=message, call=call)

    async def switch_message_delete_begin(self, message: types.Message):
        return self.interface.switch_message_delete_begin(message=message)

    async def change_message_delete_delay_begin(self, message: types.Message):
        return self.interface.change_message_delete_delay_begin(message=message)

    async def change_message_delete_delay_end(
        self, message: types.Message, state: FSMContext
    ):
        return self.interface.change_message_delete_delay_end(
            message=message, state=state
        )

    async def switch_message_delete_off(self, call: types.CallbackQuery):
        return self.interface.switch_message_delete_off(call=call)

    async def switch_message_delete_on(self, call: types.CallbackQuery):
        return self.interface.switch_message_delete_on(call=call)

    def settings_handlers_registrator(self, dp: Dispatcher):
        return self.interface.settings_handlers_registrator(dp=dp)
