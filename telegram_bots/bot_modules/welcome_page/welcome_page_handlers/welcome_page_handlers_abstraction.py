from abc import ABC
import abc
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


from bot_modules.welcome_page.welcome_page_handlers.welcome_page_handlers_interface import CustomerHandlersInterface


class CustomerHandlersAbstraction(CustomerHandlersInterface):
    def __init__(self, interface: CustomerHandlersInterface) -> None:
        self.interface = interface

    async def start_message(self, message: types.Message):
        return self.interface.state(message=message)

    def customter_welcome_page_handlers_registrator(self, dp: Dispatcher):
        return self.interface.customter_welcome_page_handlers_registrator(dp=dp)
