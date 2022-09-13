from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from bot_modules.forms.data_structures import PollQuestion, TextQuestion

from bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_interface import (
    FormsEditorHandlersInterface,
)
from bot_modules.forms.input_output_repositories import (
    currently_editing_form_repository_abs,
)
from bot_modules.forms.input_output_realisations import forms_editor_abs


class FormsEditorHandlersRealisation(FormsEditorHandlersInterface):
    class NewQuestionName(StatesGroup):
        """(rename) FSM для изменения текста 1 вопроса формы"""

        waiting_for_new_question_name = State()

    class AppendQuestion(StatesGroup):
        """(append_quest) FSM для добавления одного вопроса/ опроса в форму"""

        waiting_for_question = State()
        waiting_for_options = State()

    class EditPollOtions(StatesGroup):
        """FSM для изменения опций опроса"""

        waiting_for_options = State()

    class RenameForm(StatesGroup):
        """FSM для изменения названия формы"""

        waiting_for_name = State()

    async def edit_form_menu(self, message: types.Message):
        """Меню редактора формы"""
        form_id = int(message.text[6:])
        await forms_editor_abs.display_form(form_id=form_id, user_id=message.chat.id)

    async def rename_question_begin(self, message: types.Message, state: FSMContext):
        """(rename)(newQuestionName FSM) Берет индексы формы и вопроса из команды и спрашивает новый текст вопроса"""
        form_ids = message.text[7:].split("_")
        form_id = int(form_ids[0])
        question_id = int(form_ids[1])

        await state.update_data(form_id=form_id)
        await state.update_data(question_id=question_id)
        await message.answer("Введите измененный вопрос")
        await self.NewQuestionName.waiting_for_new_question_name.set()

    # newQuestionName.waiting_for_new_question_name
    async def rename_question_end(self, message: types.Message, state: FSMContext):
        """(rename)(newQuestionName FSM) Меняет на новый текст вопроса"""
        new_question_name = message.text
        data = await state.get_data()
        forms_editor_abs.set_new_question_name(
            form_id=data["form_id"],
            question_id=data["question_id"],
            new_question_name=new_question_name,
        )
        await forms_editor_abs.display_form(
            form_id=data["form_id"], user_id=message.chat.id
        )
        await state.finish()

    async def choose_question_type(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Предлагает выбрать тип добавляемого вопроса"""
        form_ids = message.text[10:].split("_")

        form_id = int(form_ids[0])
        question_id = int(form_ids[1])

        await state.update_data(form_id=form_id)
        await state.update_data(question_id=question_id)

        buttons = [
            types.InlineKeyboardButton(
                text="Опрос", callback_data="question_type_poll_single"
            ),
            types.InlineKeyboardButton(
                text="Ввод с клавы", callback_data="question_type_msg_single"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await message.reply("Выберите тип вопроса", reply_markup=keyboard)
        currently_editing_form_repository_abs.add_user(user_id=message.chat.id)

    # form.waiting_for_question
    async def get_question(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""

        question = message.text
        await state.update_data(question=question)
        data = await state.get_data()
        if data["type"] == "msg":
            questionData = TextQuestion(
                question_text=question, question_message_id=int(), user_answered=str()
            )
            forms_editor_abs.insert_question(
                form_id=data["form_id"],
                insert_after_id=data["question_id"],
                question=questionData,
            )

            await forms_editor_abs.display_form(
                form_id=data["form_id"], user_id=message.chat.id
            )
            await state.finish()
            currently_editing_form_repository_abs.delete_user(user_id=message.chat.id)

        else:
            await state.update_data(question=question)
            await message.reply("Пришлите варианты ответов через запятую")
            await self.AppendQuestion.waiting_for_options.set()

    # form.waiting_for_options
    async def get_options(self, message: types.Message, state: FSMContext):
        """(append_quest)(form FSM) Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""

        options = message.text.split(",")
        await state.update_data(options=options)

        data = await state.get_data()

        questionData = PollQuestion(
            question_text=data["question"],
            options=data["options"],
            question_message_id=int(),
            user_answered=str(),
        )

        forms_editor_abs.insert_question(
            form_id=data["form_id"],
            insert_after_id=data["question_id"],
            question=questionData,
        )

        await forms_editor_abs.display_form(
            form_id=data["form_id"], user_id=message.chat.id
        )
        await state.finish()
        currently_editing_form_repository_abs.delete_user(user_id=message.chat.id)

    async def question_type_poll(self, call: types.CallbackQuery, state: FSMContext):
        """(append_quest) Начало создания опроса"""

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await state.update_data(type="poll")
        await call.message.answer(
            "Введите вопрос", reply_markup=types.ReplyKeyboardRemove()
        )
        await self.AppendQuestion.waiting_for_question.set()

    async def question_type_msg(self, call: types.CallbackQuery, state: FSMContext):
        """(append_quest) Начало создания обычного вопроса"""

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await state.update_data(type="msg")
        await call.message.answer(
            "Введите вопрос", reply_markup=types.ReplyKeyboardRemove()
        )
        await self.AppendQuestion.waiting_for_question.set()

    async def remove_question_by_id(self, message: types.Message):
        """(delete_quest) Удаляет вопрос по его id"""
        form_ids = message.text[4:].split("_")

        form_id = int(form_ids[0])
        question_id = int(form_ids[1])

        forms_editor_abs.delete_question(form_id=form_id, question_id=question_id)
        await forms_editor_abs.display_form(form_id=form_id, user_id=message.chat.id)

    async def edit_poll_options_get_data(
        self, message: types.Message, state: FSMContext
    ):
        """(edit)(editPollOtions FSM) Получает id опроса для изменеия опций"""
        form_ids = message.text[5:].split("_")

        form_id = int(form_ids[0])
        question_id = int(form_ids[1])
        await state.update_data(form_id=form_id)
        await state.update_data(question_id=question_id)

        await message.answer(" Введите новые варианты ответов через запятую")
        await self.EditPollOtions.waiting_for_options.set()

    # editPollOtions.waiting_for_options
    async def edit_poll_options_set_data(
        self, message: types.Message, state: FSMContext
    ):
        """(edit)(editPollOtions FSM) Получает id опроса для изменения опций"""
        options = message.text.split(",")
        await state.update_data(options=options)

        data = await state.get_data()
        forms_editor_abs.edit_poll_options(
            form_id=data["form_id"],
            question_id=data["question_id"],
            new_poll_options=data["options"],
        )
        await forms_editor_abs.display_form(
            form_id=data["form_id"], user_id=message.chat.id
        )
        await state.finish()

    async def edit_form_name_start(self, message: types.Message, state: FSMContext):
        """(edit)(renameForm FSM) Получает новое название формы"""
        form_id = int(message.text[8:])
        await state.update_data(form_id=form_id)
        await message.answer("Введите новое название формы")
        await self.RenameForm.waiting_for_name.set()

    # renameForm.waiting_for_name
    async def edit_form_name_finish(self, message: types.Message, state: FSMContext):
        """(edit)(renameForm FSM) Изменяет название формы"""
        new_name = message.text
        data = await state.get_data()

        forms_editor_abs.set_new_form_name(form_id=data["form_id"], new_name=new_name)
        await forms_editor_abs.display_form(
            form_id=data["form_id"], user_id=message.chat.id
        )
        await state.finish()

    async def delete_form(self, message: types.Message):
        """Удаляет форму"""
        delete_id = int(message.text[5:])
        forms_editor_abs.delete_form(form_id=delete_id)

        await forms_editor_abs.display_forms_repository(user_id=message.chat.id)

    def forms_editor_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.delete_form, lambda message: message.text.startswith("/del_")
        )
        dp.register_message_handler(
            self.edit_form_menu, lambda message: message.text.startswith("/edit_")
        )
        dp.register_message_handler(
            self.edit_form_name_start,
            lambda message: message.text.startswith("/rename_"),
        )
        dp.register_message_handler(
            self.edit_form_name_finish, state=self.RenameForm.waiting_for_name
        )

        dp.register_message_handler(
            self.rename_question_begin,
            lambda message: message.text.startswith("/rename"),
        )
        dp.register_message_handler(
            self.edit_poll_options_get_data,
            lambda message: message.text.startswith("/edit"),
        )
        dp.register_message_handler(
            self.choose_question_type,
            lambda message: message.text.startswith("/add_after"),
        )
        dp.register_message_handler(
            self.remove_question_by_id, lambda message: message.text.startswith("/del")
        )
        dp.register_message_handler(
            self.rename_question_end,
            state=self.NewQuestionName.waiting_for_new_question_name,
        )

        dp.register_message_handler(
            self.get_question, state=self.AppendQuestion.waiting_for_question
        )
        dp.register_message_handler(
            self.get_options, state=self.AppendQuestion.waiting_for_options
        )
        dp.register_message_handler(
            self.edit_poll_options_set_data,
            state=self.EditPollOtions.waiting_for_options,
        )

        dp.register_callback_query_handler(
            self.question_type_poll, text="question_type_poll_single"
        )
        dp.register_callback_query_handler(
            self.question_type_msg, text="question_type_msg_single"
        )
