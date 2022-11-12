from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from bot_modules.schedule.settings.settings_handlers.settings_handlers_interface import (
    ScheduleSettingsHandlersInterface,
)

from bot_modules.schedule.settings.input_output_repositories import (
    settings_repository_abs,
)

from bot_modules.special_functions.functions_for_text_interface import (
    student_delete_previous_calls,
    student_delete_previous_messages,
)


class ScheduleSettingsHandlers(ScheduleSettingsHandlersInterface):
    class ChangeScheduleNotificationDelayFSM(StatesGroup):
        wait_for_new_delay = State()

    async def show_setting_menu(self, message: types.Message):

        user_info = settings_repository_abs.get_user_settings(user_id=message.chat.id)
        full_message = "Настройки расписания: "
        full_message += "\nОповещения о следующем предмете: " + str(
            user_info.schedule_notifications_switch
        )

        if user_info.schedule_notifications_switch:
            full_message += (
                " За " + str(user_info.schedule_notifications_delay) + " сек"
            )

        buttons = [
            types.InlineKeyboardButton(
                text="Изменить настройки", callback_data="change_schedule_settings"
            )
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        answer = await message.reply(full_message, reply_markup=keyboard)
        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=1
        )

    async def edit_setting_menu(self, call: types.CallbackQuery):
        await call.answer()
        full_message = "Изменение настроек"
        full_message += (
            "\nОповещения о следующем предмете: /set_switch_schedule_notification"
        )
        full_message += "\nСмена интервала оповещения о следующем предмете: /set_switch_schedule_notification_delay"

        answer = await call.message.answer(full_message)
        await student_delete_previous_calls(
            last_message_to_delete=answer, num_of_messages_to_delete=1
        )

    async def switch_schedule_notification_begin(self, message: types.Message):

        buttons = [
            types.InlineKeyboardButton(
                text="ВКЛ", callback_data="switch_schedule_notification_on"
            ),
            types.InlineKeyboardButton(
                text="ВЫКЛ", callback_data="switch_schedule_notification_off"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(
            "Выберите состояние оповещений о следующих парах", reply_markup=keyboard
        )

    async def change_schedule_notification_delay_begin(self, message: types.Message):
        await message.answer(
            "Выберите время до пары следующей пары, за которое будут приходить оповещения"
        )
        await self.ChangeScheduleNotificationDelayFSM.wait_for_new_delay.set()

    async def change_schedule_notification_delay_end(
        self, message: types.Message, state: FSMContext
    ):
        delay = int(message.text)
        settings_repository_abs.set_schedule_notifications_delay(
            user_id=message.chat.id, delay=delay
        )
        
        await state.finish()
        answer = await self.show_setting_menu(message=message)
        student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def switch_schedule_notification_off(self, call: types.CallbackQuery):
        await call.answer()
        settings_repository_abs.set_schedule_notifications_switch(
            user_id=call.message.chat.id, state=False
        )
        answer = await self.show_setting_menu(message=call.message)
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def switch_schedule_notification_on(self, call: types.CallbackQuery):
        await call.answer()
        settings_repository_abs.set_schedule_notifications_switch(
            user_id=call.message.chat.id, state=True
        )
        answer = await self.show_setting_menu(message=call.message)
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    def settings_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.show_setting_menu, commands="schedule_settings"
        )

        dp.register_message_handler(
            self.change_schedule_notification_delay_end,
            state=self.ChangeScheduleNotificationDelayFSM.wait_for_new_delay,
        )

        dp.register_message_handler(
            self.switch_schedule_notification_begin,
            commands="set_switch_schedule_notification",
        )

        dp.register_message_handler(
            self.change_schedule_notification_delay_begin,
            commands="set_switch_schedule_notification_delay",
        )

        dp.register_callback_query_handler(
            self.switch_schedule_notification_off,
            text="switch_schedule_notification_off",
        )
        dp.register_callback_query_handler(
            self.switch_schedule_notification_on, text="switch_schedule_notification_on"
        )

        dp.register_callback_query_handler(
            self.edit_setting_menu, text="change_schedule_settings"
        )
