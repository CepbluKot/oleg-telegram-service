from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


from bot_modules.settings.settings_handlers.settings_handlers_interface import (
    SpecialSettingsHandlersInterface,
)
# from bot_modules.special_functions.functions_for_text_interface import (
#     student_delete_previous_messages,
# )
from bot_modules.forms.settings.input_output_repositories import settings_repository_abs


class FormsSettingsHandlers(SpecialSettingsHandlersInterface):
    class ChangeScheduleNotificationDelayFSM(StatesGroup):
        wait_for_new_delay = State()

    class ChangeMessageDeleteDelayFSM(StatesGroup):
        wait_for_new_delay = State()

    async def show_setting_menu(self, message: types.Message):
        user_info = settings_repository_abs.get_user_settings(user_id=message.chat.id)
        full_message = (
            "Ваши настройки: "
            + "\nОповещения о новых формах: "
            + str(user_info.forms_notifications)
        )
        buttons = [
            types.InlineKeyboardButton(
                text="Изменить настройки", callback_data="change_forms_settings"
            )
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        answer = await message.reply(full_message, reply_markup=keyboard)
        # await student_delete_previous_messages(
        #     last_message_to_delete=answer, num_of_messages_to_delete=1
        # )

    async def edit_setting_menu(self, message: types.Message):
        full_message = "Изменение настроек"
        full_message += (
            "\nОповещения о полученной форме: /set_switch_schedule_notification"
        )
        answer = await message.answer(full_message)
        # await student_delete_previous_messages(
        #     last_message_to_delete=answer, num_of_messages_to_delete=1
        # )

    async def switch_forms_notification_begin(self, call: types.CallbackQuery):
        buttons = [
            types.InlineKeyboardButton(
                text="ВКЛ", callback_data="switch_forms_notification_on"
            ),
            types.InlineKeyboardButton(
                text="ВЫКЛ", callback_data="switch_forms_notification_off"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await call.message.answer(
            "Выберите состояние оповещений о нвых формах",
            reply_markup=keyboard,
        )

    async def switch_forms_notification_off(self, call: types.CallbackQuery):
        await call.answer()
        settings_repository_abs.set_forms_notifications_switch(
            user_id=call.message.chat.id, state=False
        )
        answer = await self.show_setting_menu(message=call.message)
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        # await student_delete_previous_messages(
        #     last_message_to_delete=answer, num_of_messages_to_delete=2
        # )

    async def switch_forms_notification_on(self, call: types.CallbackQuery):
        await call.answer()
        settings_repository_abs.set_forms_notifications_switch(
            user_id=call.message.chat.id, state=True
        )
        answer = await self.show_setting_menu(message=call.message)
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        # await student_delete_previous_messages(
        #     last_message_to_delete=answer, num_of_messages_to_delete=2
        # )

    def settings_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.show_setting_menu, commands="change_forms_settings"
        )
        dp.register_callback_query_handler(
            self.switch_forms_notification_begin, text="change_forms_settings"
        )
        dp.register_callback_query_handler(
            self.switch_forms_notification_on, text="switch_forms_notification_on"
        )
        dp.register_callback_query_handler(
            self.switch_forms_notification_off, text="switch_forms_notification_off"
        )
