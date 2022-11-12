from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_modules.schedule.settings.settings_handlers.settings_handlers_interface import (
    ScheduleSettingsHandlersInterface,
)


class ScheduleSettingsHandlersAbstraction(ScheduleSettingsHandlersInterface):
    def __init__(self, interface: ScheduleSettingsHandlersInterface) -> None:
        self.interface = interface

    async def show_setting_menu(self, message: types.Message):
        return self.interface.show_setting_menu(message=message)

    async def edit_setting_menu(self, message: types.Message):
        return self.interface.edit_setting_menu(message=message)

    async def change_schedule_notification_delay_begin(self, message: types.Message):
        return self.interface.change_message_delete_delay_begin(message=message)

    async def change_schedule_notification_delay_end(
        self, message: types.Message, state: FSMContext
    ):
        return self.interface.change_message_delete_delay_end(
            message=message, state=state
        )

    async def switch_schedule_notification_off(self, call: types.CallbackQuery):
        return self.interface.switch_message_delete_off(call=call)

    async def switch_schedule_notification_on(self, call: types.CallbackQuery):
        return self.interface.switch_message_delete_on(call=call)

    def settings_handlers_registrator(self, dp: Dispatcher):
        return self.interface.settings_handlers_registrator(dp=dp)
