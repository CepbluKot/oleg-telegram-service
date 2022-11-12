from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from bot_modules.special_functions.settings.input_output_repositories import (
    settings_repository_abs,
)
from bot_modules.special_functions.settings.settings_handlers.settings_handlers_interface import (
    SettingsHandlersInterface,
)
# from bot_modules.special_functions.functions_for_text_interface import (
#     student_delete_previous_calls,
#     student_delete_previous_messages,
# )


class SettingsHandlers(SettingsHandlersInterface):
    class ChangeMessageDeleteDelayFSM(StatesGroup):
        wait_for_new_delay = State()

    async def show_setting_menu(self, message: types.Message):
        user_info = settings_repository_abs.get_user_settings(user_id=message.chat.id)

        full_message = "Настройки удаления сообщений: "

        full_message += "\nИнтервал исчезновения сообщений: " + str(
            user_info.message_delete_switch
        )

        if user_info.message_delete_switch:
            full_message += str(user_info.message_delete_delay) + " сек"

        buttons = [
            types.InlineKeyboardButton(
                text="Изменить настройки", callback_data="change_message_settings"
            )
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        answer = await message.reply(full_message, reply_markup=keyboard)

        # await student_delete_previous_messages(
        #     last_message_to_delete=answer, num_of_messages_to_delete=1
        # )

    async def edit_setting_menu(self, call: types.CallbackQuery):
        await call.answer()
        full_message = "Изменение настроек"
        full_message += "\nИнтервал исчезновения сообщений: /set_message_delete_switch"
        full_message += "\nУдалять сообщения через: /set_message_delete_delay"
        answer = await call.message.answer(full_message)
        # await student_delete_previous_calls(
        #     last_message_to_delete=answer, num_of_messages_to_delete=1
        # )

    async def switch_message_delete_begin(self, message: types.Message):
        buttons = [
            types.InlineKeyboardButton(
                text="ВКЛ", callback_data="switch_message_delete_on"
            ),
            types.InlineKeyboardButton(
                text="ВЫКЛ", callback_data="switch_message_delete_off"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(
            "Выберите состояние автоматического удаления сообщений",
            reply_markup=keyboard,
        )

    async def change_message_delete_delay_begin(self, message: types.Message):
        await message.answer(
            "Выберите интервал после которого автоматичеси удаляются сообщения"
        )
        await self.ChangeMessageDeleteDelayFSM.wait_for_new_delay.set()

    async def change_message_delete_delay_end(
        self, message: types.Message, state: FSMContext
    ):
        delay = int(message.text)
        settings_repository_abs.set_message_delete_delay(
            user_id=message.chat.id, delay=delay
        )

        await state.finish()

        answer = await self.show_setting_menu(message=message)
        # await student_delete_previous_messages(
        #     last_message_to_delete=answer, num_of_messages_to_delete=2
        # )

    async def switch_message_delete_off(self, call: types.CallbackQuery):
        await call.answer()
        settings_repository_abs.set_message_delete_switch(
            user_id=call.message.chat.id, state=False
        )

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

        answer = await self.show_setting_menu(message=call.message)
        # await student_delete_previous_calls(
        #     last_message_to_delete=answer, num_of_messages_to_delete=2
        # )

    async def switch_message_delete_on(self, call: types.CallbackQuery):
        await call.answer()
        settings_repository_abs.set_message_delete_switch(
            user_id=call.message.chat.id, state=True
        )

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

        answer = await self.show_setting_menu(message=call.message)
        # await student_delete_previous_calls(
        #     last_message_to_delete=answer, num_of_messages_to_delete=2
        # )

    def settings_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(self.show_setting_menu, commands="message_settings")

        dp.register_message_handler(
            self.change_message_delete_delay_begin,
            commands="set_message_delete_delay",
        )

        dp.register_message_handler(
            self.change_message_delete_delay_end,
            state=self.ChangeMessageDeleteDelayFSM.wait_for_new_delay,
        )

        dp.register_message_handler(
            self.switch_message_delete_begin,
            commands="set_message_delete_switch",
        )

        dp.register_callback_query_handler(
            self.edit_setting_menu, text="change_message_settings"
        )

        dp.register_callback_query_handler(
            self.switch_message_delete_off, text="switch_message_delete_off"
        )
        dp.register_callback_query_handler(
            self.switch_message_delete_on, text="switch_message_delete_on"
        )
