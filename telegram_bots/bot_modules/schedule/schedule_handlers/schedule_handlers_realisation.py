from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from bot_modules.schedule.input_output_realisation import schedule_abs


class ScheduleHandlers:
    async def show_schedule_for_the_day(self, message: types.Message):
        schedule_for_the_day = schedule_abs.get_schedule_for_the_day(message=message)
        await message.answer(schedule_for_the_day)

    async def show_schedule_for_week(self, message: types.Message):
        schedule_for_week = schedule_abs.get_schedule_for_week(message=message)
        await message.answer(schedule_for_week)

    async def show_prepod_name(self, message: types.Message):
        prepod_name = schedule_abs.get_prepod_name(message=message)
        await message.answer(prepod_name)

    def services_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.show_schedule_for_the_day, commands="show_schedule_for_the_day"
        )

        dp.register_message_handler(
            self.show_schedule_for_week, commands="show_schedule_for_week"
        )

        dp.register_message_handler(self.show_prepod_name, commands="show_prepod_name")
