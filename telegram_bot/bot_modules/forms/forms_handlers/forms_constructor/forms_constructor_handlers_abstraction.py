from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext

from bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_interface import (
    FormsConstructorHandlersInterface,
)


class FormsConstructorHandlersAbstracation(FormsConstructorHandlersInterface):
    def __init__(self, interface: FormsConstructorHandlersInterface) -> None:
        self.interface = interface

    async def choose_form_name(self, message: types.Message, state: FSMContext):
        """(name FSM) Предлагает выбрать название формы"""
        return self.interface.choose_form_name(message=message, state=state)

    async def choose_first_question_type(
        self, message: types.Message, state: FSMContext
    ):
        """(name FSM) Запоминает название и предлагает выбрать тип первого добавляемого вопроса"""
        return self.interface.choose_first_question_type(message=message, state=state)

    async def get_question_text(self, message: types.Message, state: FSMContext):
        """(form FSM) Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""
        return self.interface.get_question_text(message=message, state=state)

    async def get_question_options(self, message: types.Message, state: FSMContext):
        """(form FSM) Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""
        return self.interface.get_question_options(message)

    async def add_question_true(self, call: types.CallbackQuery):
        """Выбор параметров для нового вопроса"""
        return self.interface.add_question_true(call=call)

    async def add_question_false(self, call: types.CallbackQuery):
        """Заканчивает создание формы"""
        return self.interface.add_question_false(call=call)

    async def question_type_poll(self, call: types.CallbackQuery, state: FSMContext):
        """Начало создания опроса"""
        return self.interface.question_type_poll(call=call, state=state)

    async def question_type_msg(self, call: types.CallbackQuery, state: FSMContext):
        """Начало создания обычного вопроса"""
        return self.interface.question_type_msg(call=call, state=state)

    async def delete_question(self, message: types.Message):
        """Удаляет одну запись из списка temp_mem по её идентификатору (из сообщения)"""
        return self.interface.delete_question(message=message)

    def forms_constructor_habdlers_registrartor(self, dp: Dispatcher):
        return self.interface.forms_constructor_habdlers_registrartor(dp=dp)
