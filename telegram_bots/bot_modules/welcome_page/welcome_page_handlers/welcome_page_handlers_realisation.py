from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from bot_modules.welcome_page.welcome_page_handlers.welcome_page_handlers_interface import CustomerHandlersInterface


class CustomerHandlers(CustomerHandlersInterface):
    async def start_message(self, message: types.Message):
        await message.answer(" Добро пожаловать: \n /register \n /status \n /settings \n /cancel")

    def customter_welcome_page_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.start_message,
            commands="start",
        )
