from abc import ABC, abstractmethod
from aiogram import types, Dispatcher
from bot_modules.schedule.schedule_realisation.schedule_interface import (
    ScheduleInterface,
)


class ScheduleAbstraction(ScheduleInterface):
    def __init__(self, interface: ScheduleInterface) -> None:
        self.interface = interface

    def get_schedule_for_the_day(self, message: types.Message):
        return self.interface.get_schedule_for_the_day(message=message)

    def get_schedule_for_week(self, message: types.Message):
        return self.get_schedule_for_week(message=message)

    def get_prepod_name(self, message: types.Message):
        return self.get_prepod_name(message=message)
