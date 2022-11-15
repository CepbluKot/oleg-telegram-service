from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from abc import ABC, abstractmethod


class SpecialSettingsHandlersInterface(ABC):
    @abstractmethod
    async def show_setting_menu(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def settings_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
