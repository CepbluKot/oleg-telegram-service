from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from bot_modules.settings.settings_handlers.settings_handlers_interface import (
    SpecialSettingsHandlersInterface,
)


class SettingsHandlersAbstraction(SpecialSettingsHandlersInterface):
    def __init__(self, interface: SpecialSettingsHandlersInterface) -> None:
        self.interface = interface

    async def show_setting_menu(self, message: types.Message):
        self.interface.edit_setting_menu(message=message)

    def settings_handlers_registrator(self, dp: Dispatcher):
        return self.interface.settings_handlers_registrator(dp=dp)
