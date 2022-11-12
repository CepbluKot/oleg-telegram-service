from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


from bot_modules.settings.settings_handlers.settings_handlers_interface import (
    SpecialSettingsHandlersInterface,
)
# from bot_modules.special_functions.functions_for_text_interface import (
#     student_delete_previous_messages,
# )
from bot_modules.settings.input_output_repositories import settings_repository_abs


class SettingsHandlers(SpecialSettingsHandlersInterface):
    async def show_setting_menu(self, message: types.Message):

        settings_repository_abs.add_user(user_id=message.chat.id)

        full_message = "Настройки"
        # full_message += "\nНастройки оповещений о расписании: /schedule_settings"
        full_message += "\nНастройки сообщений: /message_settings"
        full_message += (
            "\nНастройки оповещений о полученных формах: /change_forms_settings"
        )

        answer = await message.answer(full_message)
        # await student_delete_previous_messages(
        #     last_message_to_delete=answer, num_of_messages_to_delete=1
        # )

    def settings_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(self.show_setting_menu, commands="settings")
