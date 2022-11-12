from abc import ABC, abstractmethod
from aiogram import types, Dispatcher


class ScheduleInterface(ABC):
    @abstractmethod
    def get_schedule_for_the_day(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def get_schedule_for_week(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def get_prepod_name(self, message: types.Message):
        raise NotImplemented
