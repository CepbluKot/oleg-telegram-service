from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_interface import (
    FormsEditorHandlersInterface,
)


class FormsEditorHandlersAbstraction(FormsEditorHandlersInterface):
    def __init__(self, interface: FormsEditorHandlersInterface) -> None:
        self.interface = interface

    async def edit_form_menu(self, message: types.Message):
        """Меню редактора формы"""
        self.interface.edit_form_menu(message=message)

    async def rename_question_begin(self, message: types.Message, state: FSMContext):
        """(rename)(newQuestionName FSM) Берет индексы формы и вопроса из команды и спрашивает новый текст вопроса"""
        self.interface.rename_question_begin(message=message, state=state)

    # newQuestionName.waiting_for_new_question_name
    async def rename_question_end(self, message: types.Message, state: FSMContext):
        """(rename)(newQuestionName FSM) Меняет на новый текст вопроса"""
        self.interface.rename_question_end(message=message, state=state)

    async def choose_question_type(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Предлагает выбрать тип добавляемого вопроса"""
        self.interface.choose_question_type(message=message, state=state)

    # form.waiting_for_question
    async def get_question(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""
        self.interface.get_question(message=message, state=state)

    # form.waiting_for_options
    async def get_options(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""
        self.interface.get_options(message=message, state=state)

    async def question_type_poll(self, call: types.CallbackQuery, state: FSMContext):
        """(append_quest) Начало создания опроса"""
        self.interface.question_type_poll(call=call, state=state)

    async def question_type_msg(self, call: types.CallbackQuery, state: FSMContext):
        """(append_quest) Начало создания обычного вопроса"""
        self.interface.question_type_msg(call=call, state=state)

    async def remove_question_by_id(self, message: types.Message):
        """(delete_quest) Удаляет вопрос по его id"""
        self.interface.remove_question_by_id(message=message)

    async def edit_poll_options_get_data(
        self, message: types.Message, state: FSMContext
    ):
        """(edit)(editPollOtions FSM) Получает id опроса для изменеия опций"""
        self.interface.edit_poll_options_get_data(message=message, state=state)

    # editPollOtions.waiting_for_options
    async def edit_poll_options_set_data(
        self, message: types.Message, state: FSMContext
    ):
        """(edit)(editPollOtions FSM) Получает id опроса для изменеия опций"""
        self.interface.edit_poll_options_set_data(message=message, state=state)

    async def edit_form_name_start(self, message: types.Message, state: FSMContext):
        """(edit)(renameForm FSM) Получает новое название формы"""
        self.interface.edit_form_name_start(message=message, state=state)

    # renameForm.waiting_for_name
    async def edit_form_name_finish(self, message: types.Message, state: FSMContext):
        """(edit)(renameForm FSM) Изменяет название формы"""
        self.interface.edit_form_name_finish(message=message, state=state)

    async def delete_form(self, message: types.Message):
        """Удаляет форму"""
        self.interface.delete_form(message=message)

    def forms_editor_handlers_registrator(self, dp: Dispatcher):
        self.interface.forms_editor_handlers_registrator(dp=dp)
