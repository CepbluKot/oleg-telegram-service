from abc import ABC, abstractmethod
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_modules.schedule.input_output_realisation import schedule_abs
from bot_modules.schedule.schedule_handlers.schedule_handlers_interface import (
    ScheduleHandlersInterface,
)


class ScheduleHandlersAbstraction(ScheduleHandlersInterface):
    def __init__(self, interface: ScheduleHandlersInterface) -> None:
        self.interface = interface

    async def show_schedule_for_the_day(self, message: types.Message):
        return self.interface.show_schedule_for_the_day(message=message)

    async def show_schedule_for_week(self, message: types.Message):
        return self.interface.show_schedule_for_week(message=message)

    async def show_prepod_name(self, message: types.Message):
        return self.interface.show_prepod_name(message=message)

    def services_handlers_registrator(self, dp: Dispatcher):
        return self.interface.services_handlers_registrator(dp=dp)
