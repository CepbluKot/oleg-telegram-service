""" Система опросов"""

""" Создается форма, добавляется в хранилище форм"""


from abc import ABC, abstractmethod
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


class FormsConstructorHandlersInterface(ABC):
    @abstractmethod
    async def choose_form_name(self, message: types.Message, state: FSMContext):
        """(name FSM) Предлагает выбрать название формы"""
        raise NotImplemented

    @abstractmethod
    async def choose_first_question_type(
        self, message: types.Message, state: FSMContext
    ):
        raise NotImplemented

    @abstractmethod
    async def get_question_text(self, message: types.Message, state: FSMContext):
        raise NotImplemented

    @abstractmethod
    async def get_question_options(self, message: types.Message, state: FSMContext):
        raise NotImplemented

    @abstractmethod
    async def add_question_true(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def add_question_false(self, call: types.CallbackQuery):
        raise NotImplemented

    @abstractmethod
    async def question_type_poll(self, call: types.CallbackQuery, state: FSMContext):
        raise NotImplemented

    @abstractmethod
    async def question_type_msg(self, call: types.CallbackQuery, state: FSMContext):
        raise NotImplemented

    @abstractmethod
    async def delete_question(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def forms_constructor_habdlers_registrartor(self, dp: Dispatcher):
        raise NotImplemented
