from abc import ABC, abstractmethod
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext


class FormsMenuHandlersInterface(ABC):
    @abstractmethod
    async def choose_groups(self, message: types.Message, state: FSMContext):
        """Спрашивает юзера"""
        raise NotImplemented

    @abstractmethod
    async def display_forms_repository(self, message: types.message):
        raise NotImplemented

    @abstractmethod
    def lambda_checker_poll(self, poll_answer: types.PollAnswer):
        """Проверяет опрос"""
        raise NotImplemented

    @abstractmethod
    async def poll_handler(self, poll_answer: types.PollAnswer):
        """Активируется, когда приходит ответ на опрос/ опрос закрывается"""
        raise NotImplemented

    @abstractmethod
    def forms_menu_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
