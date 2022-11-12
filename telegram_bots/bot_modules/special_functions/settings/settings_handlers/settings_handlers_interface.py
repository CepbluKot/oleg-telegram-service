from abc import ABC, abstractmethod
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot_modules.special_functions.settings.input_output_repositories import (
    settings_repository_abs,
)


class SettingsHandlersInterface(ABC):
    @abstractmethod
    async def show_setting_menu(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def edit_setting_menu(
        self, message: types.Message, call: types.CallbackQuery
    ):
        raise NotImplemented

    @abstractmethod
    async def switch_message_delete_begin(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def change_message_delete_delay_begin(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def change_message_delete_delay_end(
        self, message: types.Message, state: FSMContext
    ):
        raise NotImplemented

    @abstractmethod
    async def switch_message_delete_off(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def switch_message_delete_on(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    def settings_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
