from abc import ABC
import abc
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class CustomerHandlersInterface(ABC):
    @abc.abstractclassmethod
    async def start_message(self, message: types.Message):
        raise NotImplemented

    @abc.abstractclassmethod
    def customter_welcome_page_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
