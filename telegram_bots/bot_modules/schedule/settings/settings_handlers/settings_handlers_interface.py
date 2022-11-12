from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from abc import ABC, abstractmethod


class ScheduleSettingsHandlersInterface(ABC):
    @abstractmethod
    async def show_setting_menu(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def edit_setting_menu(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def change_schedule_notification_delay_begin(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def change_schedule_notification_delay_end(
        self, message: types.Message, state: FSMContext
    ):
        raise NotImplemented

    @abstractmethod
    async def switch_schedule_notification_off(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def switch_schedule_notification_on(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    def settings_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
