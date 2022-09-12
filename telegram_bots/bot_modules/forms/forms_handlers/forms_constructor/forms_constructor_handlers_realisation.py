""" Система опросов"""

""" Создается форма, добавляется в хранилище форм"""


from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_interface import (
    FormsConstructorHandlersInterface,
)
from bot_modules.forms.data_structures import Form, PollQuestion, TextQuestion


from bot_modules.register.input_output_repositories import register_repository_abs
from bot_modules.forms.input_output_repositories import (
    currently_editing_form_repository_abs,
)
from bot_modules.forms.input_output_realisations import forms_constructor_abs


class FormsConstructorHandlersRealisation(FormsConstructorHandlersInterface):
    class ChooseFormNameFSM(StatesGroup):
        """FSM для выбора названия опроса"""

        waiting_for_form_name = State()

    class AddQuestionFSM(StatesGroup):
        """FSM для добавления одного вопроса/ опроса в форму"""

        waiting_for_question_text = State()
        waiting_for_options = State()

    async def choose_form_name(self, message: types.Message):
        """(name FSM) Предлагает выбрать название формы"""
        await message.reply("Выберите название формы")
        await self.ChooseFormNameFSM.waiting_for_form_name.set()

    async def choose_first_question_type(
        self, message: types.Message, state: FSMContext
    ):
        """(name FSM) Запоминает название и предлагает выбрать тип первого добавляемого вопроса"""
        form_data = Form(
            form_id=forms_constructor_abs.generate_form_id(),
            form_name=str(message.text),
            creator=register_repository_abs.get_user_data(user_id=message.chat.id),
            questions=list(),
        )

        forms_constructor_abs.add_form(form=form_data)

        buttons = [
            types.InlineKeyboardButton(
                text="Опрос", callback_data="question_type_poll"
            ),
            types.InlineKeyboardButton(
                text="Ввод с клавы", callback_data="question_type_msg"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await message.reply("Выберите тип вопроса", reply_markup=keyboard)
        await state.finish()

    async def get_question_text(self, message: types.Message, state: FSMContext):
        """(form FSM) Получает текст вопроса и тип, затем ЗАПОМИНАЕТ (и предлагает ввести варианты ответов)
        и предлагает добавить вопрос"""

        question = message.text
        await state.update_data(question=question)
        data = await state.get_data()
        if data["type"] == "msg":

            question_data = TextQuestion(
                question_text=question, question_message_id=int(), user_answered=str()
            )

            forms_constructor_abs.add_text_question_to_form(
                text_question=question_data, user_id=message.chat.id
            )

            buttons = [
                types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
                types.InlineKeyboardButton(text="Нет", callback_data="add_quest_false"),
            ]

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            await forms_constructor_abs.display_form(user_id=message.chat.id)

            await message.reply("Добавить ещё 1 вопрос?", reply_markup=keyboard)
            await state.finish()

        else:
            await state.update_data(question=question)
            await message.reply("Пришлите варианты ответов через запятую")
            await self.AddQuestionFSM.waiting_for_options.set()

    async def get_question_options(self, message: types.Message, state: FSMContext):
        """(form FSM) Получает варианты ответов, ЗАПОМИНАЕТ и предлагает добавить вопрос"""

        options = message.text.split(",")
        await state.update_data(options=options)

        user_data = await state.get_data()
        poll_data = PollQuestion(
            question_text=user_data["question"],
            options=user_data["options"],
            question_message_id=int(),
            user_answered=str(),
        )
        forms_constructor_abs.add_poll_question_to_form(
            poll_question=poll_data, user_id=message.chat.id
        )

        buttons = [
            types.InlineKeyboardButton(text="Да", callback_data="add_quest_true"),
            types.InlineKeyboardButton(text="Нет", callback_data="add_quest_false"),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await forms_constructor_abs.display_form(user_id=message.chat.id)

        await message.reply("Добавить ещё 1 вопрос?", reply_markup=keyboard)
        await state.finish()

    async def add_question_true(self, call: types.CallbackQuery):
        """Выбор параметров для нового вопроса"""

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        buttons = [
            types.InlineKeyboardButton(
                text="Опрос", callback_data="question_type_poll"
            ),
            types.InlineKeyboardButton(
                text="Ввод с клавы", callback_data="question_type_msg"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await call.message.reply("Выберите тип вопроса", reply_markup=keyboard)

    async def add_question_false(self, call: types.CallbackQuery):
        """Заканчивает создание формы"""

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

        await forms_constructor_abs.display_form(user_id=call.message.chat.id)

        finalForm = forms_constructor_abs.get_form(user_id=call.message.chat.id)
        forms_constructor_abs.add_form_to_forms_repository(form=finalForm)

        forms_constructor_abs.delete_form(user_id=call.message.chat.id)

        await call.message.answer(
            "Форма создана", reply_markup=types.ReplyKeyboardRemove()
        )

    async def question_type_poll(self, call: types.CallbackQuery, state: FSMContext):
        """Начало создания опроса"""

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await state.update_data(type="poll")
        await call.message.answer(
            "Введите вопрос", reply_markup=types.ReplyKeyboardRemove()
        )
        await self.AddQuestionFSM.waiting_for_question_text.set()

    async def question_type_msg(self, call: types.CallbackQuery, state: FSMContext):
        """Начало создания обычного вопроса"""
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await state.update_data(type="msg")
        await call.message.answer(
            "Введите вопрос", reply_markup=types.ReplyKeyboardRemove()
        )
        await self.AddQuestionFSM.waiting_for_question_text.set()

    async def delete_question(self, message: types.Message):
        """Удаляет одну запись из списка temp_mem по её идентификатору (из сообщения)"""

        delete_id = int(message.text[4:])

        forms_constructor_abs.delete_question(
            question_id=int(delete_id), user_id=message.chat.id
        )

        await message.answer(
            "удалил пункт " + str(delete_id), reply_markup=types.ReplyKeyboardRemove()
        )
        await forms_constructor_abs.display_form(user_id=message.chat.id)

    def forms_constructor_exceptions(self, user_id: int):
        return not forms_constructor_abs.check_is_user_is_creating_form(
            user_id=user_id
        ) and not currently_editing_form_repository_abs.check_is_user_in_list(
            user_id=user_id
        )

    def forms_constructor_habdlers_registrartor(self, dp: Dispatcher):
        dp.register_message_handler(
            self.choose_form_name,
            lambda message: self.forms_constructor_exceptions(user_id=message.chat.id),
            commands="multi_form",
        )

        dp.register_message_handler(
            self.choose_first_question_type,
            state=self.ChooseFormNameFSM.waiting_for_form_name,
        )
        dp.register_message_handler(
            self.get_question_text, state=self.AddQuestionFSM.waiting_for_question_text
        )
        dp.register_message_handler(
            self.get_question_options, state=self.AddQuestionFSM.waiting_for_options
        )

        dp.register_callback_query_handler(
            self.add_question_true, text="add_quest_true"
        )
        dp.register_callback_query_handler(
            self.add_question_false, text="add_quest_false"
        )
        dp.register_callback_query_handler(
            self.question_type_poll, text="question_type_poll"
        )
        dp.register_callback_query_handler(
            self.question_type_msg, text="question_type_msg"
        )

        dp.register_message_handler(
            self.delete_question, lambda message: message.text.startswith("/del")
        )
