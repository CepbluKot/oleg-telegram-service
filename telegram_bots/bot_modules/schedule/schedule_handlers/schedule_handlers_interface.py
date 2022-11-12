from abc import ABC, abstractmethod
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_modules.schedule.input_output_realisation import schedule_abs


class ScheduleHandlersInterface(ABC):
    @abstractmethod
    async def show_schedule_for_the_day(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def show_schedule_for_week(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def show_prepod_name(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def services_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
