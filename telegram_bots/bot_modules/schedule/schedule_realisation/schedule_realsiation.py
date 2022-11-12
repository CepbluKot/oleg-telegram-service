from aiogram import types, Dispatcher

from bot_modules.schedule.schedule_realisation.schedule_interface import (
    ScheduleInterface,
)


class ScheduleRealisation(ScheduleInterface):
    def get_schedule_for_the_day(self, message: types.Message):
        return "raspisanie"

    def get_schedule_for_week(self, message: types.Message):
        return "weekly"

    def get_prepod_name(self, message: types.Message):
        return "preped"
