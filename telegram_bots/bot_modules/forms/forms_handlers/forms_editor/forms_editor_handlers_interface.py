from abc import ABC, abstractmethod
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


class FormsEditorHandlersInterface(ABC):
    @abstractmethod
    async def edit_form_menu(self, message: types.Message):
        """Меню редактора формы"""
        raise NotImplemented

    @abstractmethod
    async def rename_question_begin(self, message: types.Message, state: FSMContext):
        """(rename)(newQuestionName FSM) Берет индексы формы и вопроса из команды и спрашивает новый текст вопроса"""
        raise NotImplemented

    @abstractmethod
    # newQuestionName.waiting_for_new_question_name
    async def rename_question_end(self, message: types.Message, state: FSMContext):
        """(rename)(newQuestionName FSM) Меняет на новый текст вопроса"""
        raise NotImplemented

    @abstractmethod
    async def choose_question_type(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Предлагает выбрать тип добавляемого вопроса"""
        raise NotImplemented

    @abstractmethod
    # form.waiting_for_question
    async def get_question(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""
        raise NotImplemented

    @abstractmethod
    # form.waiting_for_options
    async def get_options(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""
        raise NotImplemented

    @abstractmethod
    async def question_type_poll(self, call: types.CallbackQuery, state: FSMContext):
        """(append_quest) Начало создания опроса"""
        raise NotImplemented

    @abstractmethod
    async def question_type_msg(self, call: types.CallbackQuery, state: FSMContext):
        """(append_quest) Начало создания обычного вопроса"""
        raise NotImplemented

    @abstractmethod
    async def remove_question_by_id(self, message: types.Message):
        """(delete_quest) Удаляет вопрос по его id"""
        raise NotImplemented

    @abstractmethod
    async def edit_poll_options_get_data(
        self, message: types.Message, state: FSMContext
    ):
        """(edit)(editPollOtions FSM) Получает id опроса для изменеия опций"""
        raise NotImplemented

    @abstractmethod
    # editPollOtions.waiting_for_options
    async def edit_poll_options_set_data(
        self, message: types.Message, state: FSMContext
    ):
        """(edit)(editPollOtions FSM) Получает id опроса для изменеия опций"""
        raise NotImplemented

    @abstractmethod
    async def edit_form_name_start(self, message: types.Message, state: FSMContext):
        """(edit)(renameForm FSM) Получает новое название формы"""
        raise NotImplemented

    @abstractmethod
    # renameForm.waiting_for_name
    async def edit_form_name_finish(self, message: types.Message, state: FSMContext):
        """(edit)(renameForm FSM) Изменяет название формы"""
        raise NotImplemented

    @abstractmethod
    async def delete_form(self, message: types.Message):
        """Удаляет форму"""
        raise NotImplemented

    @abstractmethod
    def forms_editor_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
