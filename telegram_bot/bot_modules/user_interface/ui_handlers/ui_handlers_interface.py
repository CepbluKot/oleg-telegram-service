""" Статус пользователя"""
from abc import ABC, abstractmethod
from aiogram import Dispatcher, types


class PrepodHandlersStatusInterface(ABC):
    @abstractmethod
    async def choose_ui_type(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def set_ui_type_gui(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def set_ui_type_text(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def display_user_status(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def get_form_result(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def register_handlers_prepod_status(self, dp: Dispatcher):
        raise NotImplemented


class StudentHandlersStatusInterface(ABC):
    @abstractmethod
    async def choose_ui_type(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def set_ui_type_gui(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def set_ui_type_text(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def display_user_status(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def complete_form(self, message: types.Message):
        """Получает название формы, добавляет данные в forms_dispatcher,
        запускает отправку вопросов из нужной формы"""
        raise NotImplemented

    @abstractmethod
    async def go_cycle(self, message, type):
        """Отсылает вопросы/ опросы из completing_forms_dispatcher при вызове"""
        raise NotImplemented

    @abstractmethod
    def lambda_checker_poll(self, poll_answer: types.PollAnswer):
        """Проверяет принадлежит ли опрос выбранной форме"""
        raise NotImplemented

    @abstractmethod
    def lambda_checker_msg(self, message: types.Message):
        """Проверяет является ли сообщение ответом на вопрос из формы"""
        raise NotImplemented

    @abstractmethod
    async def poll_handler(self, poll_answer: types.PollAnswer):
        """Активируется, когда приходит ответ на опрос/ опрос закрывается"""
        raise NotImplemented

    @abstractmethod
    async def msg_handler(self, message: types.Message):
        """Активируется, когда приходит сообщение"""
        raise NotImplemented

    @abstractmethod
    def check_is_already_completed(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def already_completed_message_reply(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def register_handlers_student_status(self, dp: Dispatcher):
        raise NotImplemented
