from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from bot_modules.register.data_structures import Student, Prepod

from bot_modules.register.register_handlers.register_handlers_interface import (
    PrepodHandlersInterface,
    StudentHandlersInterface,
)

from bot_modules.special_functions.functions_for_text_interface import (
    student_delete_previous_calls,
    student_delete_previous_messages,
)

from bot_modules.register.input_output_repositories import (
    currently_changing_register_data_repository_abs,
)
from bot_modules.register.input_output_realisations import (
    register_abs,
    register_edit_prepod_abs,
    register_edit_student_abs,
)
from bot_modules.forms.input_output_repositories import (
    choosing_groups_dispatcher_abs,
    currently_editing_form_repository_abs,
)
from bot_modules.service_info.input_output_repositories import groups_repository_abs
from bot_modules.forms.input_output_realisations import forms_constructor_abs


class PrepodHandlers(PrepodHandlersInterface):
    class RegisterUserFSM(StatesGroup):
        "FSM для регистрации пользователя"
        ask_for_fio = State()
        waiting_for_fio = State()

    class RegisterChangeFioFSM(StatesGroup):
        "FSM для смены ФИО пользователя"
        waiting_for_new_fio = State()

    async def not_confirmed(self, message: types.Message):
        await message.answer(" Ваши рег. данные еще не подтверждены")

    async def already_registered(self, message: types.Message):
        "Проверяет, зарегистрирован ли пользователь"
        if register_abs.get_user_data(user_id=message.chat.id).role == "student":
            await message.answer("Студент, топай регаться в свой бот, понятно да")
            return

        prepod_data = register_abs.get_user_data(user_id=message.chat.id)
        await message.answer(
            "Вы уже зарегистрированы"
            + "\nВы: "
            + str(prepod_data.fio)
            + "; "
            + "Ваша роль: "
            + str(prepod_data.role),
            reply_markup=types.ReplyKeyboardRemove(),
        )

        buttons = [
            types.InlineKeyboardButton(text="Да", callback_data="register_change_true"),
            types.InlineKeyboardButton(
                text="Нет", callback_data="register_change_false"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer("Хотите изменить рег. данные?", reply_markup=keyboard)

    async def ask_register_fio(self, message: types.message, state: FSMContext):
        "(RegisterUserFSM) Предлагаем ввести ФИО"
        await state.update_data(chosen_role="prepod")
        await message.answer("Введите ФИО")
        await self.RegisterUserFSM.waiting_for_fio.set()

    async def register_fio_chosen(self, message: types.Message, state: FSMContext):
        "(registerUser FSM) Получаем ФИО и отправляем данные"
        fio = message.text
        await state.update_data(chosen_fio=fio)
        user_data = await state.get_data()
        await message.reply(
            "Ваше ФИО: "
            + user_data["chosen_fio"]
            + "; Ваша роль: "
            + user_data["chosen_role"]
        )

        prepod_data = Prepod(
            user_id=message.chat.id,
            fio=user_data["chosen_fio"],
            role=user_data["chosen_role"],
            is_register_approved=True,
            related_groups=[],
        )

        register_abs.add_user(user=prepod_data)
        await message.answer(
            "Рег. данные отправлены на проверку",
            reply_markup=types.ReplyKeyboardRemove(),
        )
        await state.finish()

    async def register_change_true(self, call: types.CallbackQuery):
        "(already_registered Func) Выбираем какие рег. данные изменить"
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

        buttons = [
            types.InlineKeyboardButton(text="ФИО", callback_data="register_change_fio"),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await call.message.answer("Что именно изменить?", reply_markup=keyboard)
        currently_changing_register_data_repository_abs.add_user(
            user_id=call.from_user.id
        )

    async def register_change_false(self, call: types.CallbackQuery):
        "(already_registered Func) Не меняем рег. данные"
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await call.message.answer("Окес, ничего не меняем")
        currently_changing_register_data_repository_abs.delete_user(
            user_id=call.from_user.id
        )

    async def ask_edited_fio(self, call: types.CallbackQuery):
        "(register_change_true Func) Предлагаем ввести новую фамилию"
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await self.RegisterChangeFioFSM.waiting_for_new_fio.set()
        await call.message.answer("Введите новые ФИО")

    async def set_edited_fio(self, message: types.Message, state: FSMContext):
        "(register_change_fio_fsm FSM) Получаем новую фамилию и обновляем данные"
        new_fio = message.text
        register_edit_prepod_abs.set_new_fio(user_id=message.chat.id, new_fio=new_fio)
        await state.finish()
        prepod_data = register_abs.get_user_data(user_id=message.chat.id)
        await message.answer(
            "Обновленные данные отправлены на проверку: "
            + "\nВы: "
            + str(prepod_data.fio),
            reply_markup=types.ReplyKeyboardRemove(),
        )
        currently_changing_register_data_repository_abs.delete_user(
            user_id=message.chat.id
        )

    async def not_registered(self, message: types.Message):
        await message.answer(" Вы еще не зарегистрированы, используйте /register")

    def already_registered_exceptions(self, user_id: int):
        return (
            not forms_constructor_abs.check_is_user_is_creating_form(user_id=user_id)
            and register_abs.check_is_user_in_register_data(user_id=user_id)
            and not currently_changing_register_data_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
            and not choosing_groups_dispatcher_abs.is_user_in_list(user_id=user_id)
            and not currently_editing_form_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
        )

    def not_confirmed_register_exceptions(self, user_id: int):
        return (
            register_abs.check_is_user_in_register_data(user_id=user_id)
            and not register_abs.get_user_data(user_id=user_id).is_register_approved
            and not currently_changing_register_data_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
        )

    def register_exceptions(self, user_id: int):
        return (
            not forms_constructor_abs.check_is_user_is_creating_form(user_id=user_id)
            and not currently_changing_register_data_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
            and not currently_editing_form_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
        )

    def not_registered_exceptions(self, user_id):
        return not register_abs.check_is_user_in_register_data(user_id=user_id)

    def prepod_registration_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.already_registered,
            lambda message: self.already_registered_exceptions(user_id=message.chat.id),
            commands="register",
        )

        dp.register_message_handler(
            self.not_confirmed,
            lambda message: self.not_confirmed_register_exceptions(
                user_id=message.chat.id
            ),
            commands="*",
        )

        dp.register_message_handler(
            self.ask_register_fio,
            lambda message: self.register_exceptions(user_id=message.chat.id),
            commands="register",
        )

        dp.register_message_handler(
            self.register_fio_chosen, state=self.RegisterUserFSM.waiting_for_fio
        )

        dp.register_message_handler(
            self.set_edited_fio, state=self.RegisterChangeFioFSM.waiting_for_new_fio
        )

        dp.register_message_handler(
            self.not_registered,
            lambda message: self.not_registered_exceptions(user_id=message.chat.id),
        )

        dp.register_callback_query_handler(
            self.register_change_true, text="register_change_true"
        )
        dp.register_callback_query_handler(
            self.register_change_false, text="register_change_false"
        )
        dp.register_callback_query_handler(
            self.ask_edited_fio, text="register_change_fio"
        )

        # dp.register_message_handler(strangeMessagesHandler, lambda message: message.text in get_all_groups() or '; id ' in message.text)


class StudentHandlers(StudentHandlersInterface):
    class RegisterUserFSM(StatesGroup):
        "FSM для регистрации пользователя"
        ask_for_fio = State()
        waiting_for_Fio = State()
        waiting_for_group = State()

    class RegisterChangeFioFSM(StatesGroup):
        "FSM для смены ФИО пользователя"
        waiting_for_new_fio = State()

    class RegisterChangeGroupFSM(StatesGroup):
        "FSM для смены группы пользователя"
        waiting_for_new_group = State()

    async def not_confirmed(self, message: types.Message):
        await message.answer(" Ваши рег. данные еще не подтверждены")

    async def already_registered(self, message: types.Message):
        "Проверяет, зарегистрирован ли пользователь"

        if register_abs.get_user_data(user_id=message.chat.id).role == "prepod":
            answer = await message.answer(
                "Препод, топай регаться в свой бот, понятно да"
            )

            await student_delete_previous_messages(
                last_message_to_delete=answer, num_of_messages_to_delete=2
            )
            return

        student_data = register_abs.get_user_data(user_id=message.chat.id)
        await message.answer(
            "Вы уже зарегистрированы: "
            + "\nВы: "
            + str(student_data.fio)
            + "; "
            + "Ваша группа: "
            + str(student_data.group + " Ваша роль: " + str(student_data.role)),
            reply_markup=types.ReplyKeyboardRemove(),
        )

        buttons = [
            types.InlineKeyboardButton(text="Да", callback_data="register_change_true"),
            types.InlineKeyboardButton(
                text="Нет", callback_data="register_change_false"
            ),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        answer = await message.answer(
            "Хотите изменить рег. данные?", reply_markup=keyboard
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=3
        )

    async def ask_register_fio(self, message: types.message, state: FSMContext):
        "(registerUser FSM) Вводим фио"
        await state.update_data(chosen_role="student")
        await message.answer("Введите ФИО")
        await self.RegisterUserFSM.waiting_for_Fio.set()

    async def register_fio_chosen(self, message: types.Message, state: FSMContext):
        fio = message.text
        await state.update_data(chosen_fio=fio)

        marakap = ReplyKeyboardMarkup(one_time_keyboard=True)

        for data in groups_repository_abs.get_all_groups():
            marakap.add(KeyboardButton(data))

        await message.reply("Выберите группу", reply_markup=marakap)
        await self.RegisterUserFSM.waiting_for_group.set()

    async def wrong_group(self, message: types.Message):
        "(registerUser FSM) Срабатывает, если выбрана неверная группа"

        answer = await message.reply("Выберите группу из списка")
        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def register_group_chosen(self, message: types.Message, state: FSMContext):
        "(registerUser FSM) Получаем группу и добавляем пользователя в хранилище"
        user_data = await state.get_data()
        group = message.text
        await state.update_data(chosen_group=group)
        user_data = await state.get_data()
        await message.answer(
            "Ваше ФИО: "
            + user_data["chosen_fio"]
            + "; Ваша группа: "
            + user_data["chosen_group"]
            + "; Ваша роль: "
            + user_data["chosen_role"],
            reply_markup=types.ReplyKeyboardRemove(),
        )

        student_data = Student(
            user_id=message.chat.id,
            fio=user_data["chosen_fio"],
            is_register_approved=True,  # !!!!!!!!!!!
            group=user_data["chosen_group"],
        )

        register_abs.add_user(user=student_data)
        answer = await message.answer(
            "Рег. данные отправлены на проверку",
            reply_markup=types.ReplyKeyboardRemove(),
        )

        await state.finish()

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def register_change_true(self, call: types.CallbackQuery):
        "(already_registered Func) Выбираем какие рег. данные изменить"
        currently_changing_register_data_repository_abs.add_user(
            user_id=call.from_user.id
        )
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

        buttons = [
            types.InlineKeyboardButton(text="ФИО", callback_data="register_change_fio"),
            types.InlineKeyboardButton(
                text="Группу", callback_data="register_change_group"
            ),
        ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await call.message.answer("Что именно изменить?", reply_markup=keyboard)

    async def register_change_false(self, call: types.CallbackQuery):
        "(already_registered Func) Не меняем рег. данные"
        await call.answer()
        await student_delete_previous_calls(
            last_message_to_delete=call, num_of_messages_to_delete=1
        )
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        answer = await call.message.answer("Окес, ничего не меняем")
        currently_changing_register_data_repository_abs.delete_user(
            user_id=call.from_user.id
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=1
        )

    async def ask_edited_fio(self, call: types.CallbackQuery):
        "(register_change_true Func) Предлагаем ввести новую фамилию"
        await call.answer()
        await student_delete_previous_calls(
            last_message_to_delete=call, num_of_messages_to_delete=1
        )
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await self.RegisterChangeFioFSM.waiting_for_new_fio.set()
        await call.message.answer("Введите новые ФИО")

    async def set_edited_fio(self, message: types.Message, state: FSMContext):
        "(register_change_fio_fsm FSM) Получаем новую фамилию и обновляем данные"
        new_fio = message.text
        register_edit_student_abs.set_new_fio(new_fio=new_fio, user_id=message.chat.id)
        await state.finish()

        editedStudentData = register_edit_student_abs.get_user_data(
            user_id=message.chat.id
        )
        answer = await message.answer(
            "Обновленные данные отправлены на проверку: "
            + "\nВы: "
            + str(editedStudentData.fio)
            + "; "
            + "Ваша группа: "
            + str(editedStudentData.group),
            reply_markup=types.ReplyKeyboardRemove(),
        )
        currently_changing_register_data_repository_abs.delete_user(
            user_id=message.chat.id
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=3
        )

    async def ask_edited_group(self, call: types.CallbackQuery):
        "(register_change_true Func) Предлагаем ввести новую группу"
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

        marakap = ReplyKeyboardMarkup(one_time_keyboard=True)
        for data in groups_repository_abs.get_all_groups():
            marakap.add(KeyboardButton(data))
        await self.RegisterChangeGroupFSM.waiting_for_new_group.set()
        await call.message.reply("chos u rgrup", reply_markup=marakap)

    async def set_edited_group(self, message: types.Message, state: FSMContext):
        "(register_change_group_fsm FSM) Получаем новую группу и обновляем данные"
        new_group = message.text
        register_edit_student_abs.set_new_group(
            new_group=new_group, user_id=message.chat.id
        )
        await state.finish()

        edited_student_data = register_edit_student_abs.get_user_data(
            user_id=message.chat.id
        )
        answer = await message.answer(
            "Обновленные данные отправлены на проверку: "
            + "\nВы: "
            + str(edited_student_data.fio)
            + "; "
            + "Ваша группа: "
            + str(edited_student_data.group),
            reply_markup=types.ReplyKeyboardRemove(),
        )
        currently_changing_register_data_repository_abs.delete_user(
            user_id=message.chat.id
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=4
        )

    async def not_registered(self, message: types.Message):
        answer = await message.answer(
            " Вы еще не зарегистрированы, используйте /register"
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    def alreadyRegisteredExceptions(self, user_id: int):
        return register_abs.check_is_user_in_register_data(
            user_id=user_id
        ) and not currently_changing_register_data_repository_abs.check_is_user_in_list(
            user_id=user_id
        )

    def notConfirmedRegisterExceptions(self, user_id: int):
        return (
            register_abs.check_is_user_in_register_data(user_id=user_id)
            and not register_abs.get_user_data(user_id=user_id).is_register_approved
            and not currently_changing_register_data_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
        )

    def registerExceptions(self, user_id: int):
        return (
            not currently_changing_register_data_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
        )

    def notRegisteredExceptions(self, user_id):
        return not register_abs.check_is_user_in_register_data(user_id=user_id)

    def student_registration_handlers_register(self, dp: Dispatcher):
        dp.register_message_handler(
            self.already_registered,
            lambda message: self.alreadyRegisteredExceptions(user_id=message.chat.id),
            commands="register",
        )

        dp.register_message_handler(
            self.not_confirmed,
            lambda message: self.notConfirmedRegisterExceptions(
                user_id=message.chat.id
            ),
            commands="*",
        )

        dp.register_message_handler(
            self.ask_register_fio,
            lambda message: self.registerExceptions(user_id=message.chat.id),
            commands="register",
        )

        dp.register_message_handler(
            self.register_fio_chosen, state=self.RegisterUserFSM.waiting_for_Fio
        )

        dp.register_message_handler(
            self.wrong_group,
            lambda message: message.text not in groups_repository_abs.get_all_groups(),
            state=self.RegisterUserFSM.waiting_for_group,
        )

        dp.register_message_handler(
            self.register_group_chosen,
            lambda message: message.text in groups_repository_abs.get_all_groups(),
            state=self.RegisterUserFSM.waiting_for_group,
        )

        dp.register_message_handler(
            self.wrong_group,
            lambda message: message.text not in groups_repository_abs.get_all_groups(),
            state=self.RegisterChangeGroupFSM.waiting_for_new_group,
        )

        dp.register_message_handler(
            self.set_edited_group,
            lambda message: message.text in groups_repository_abs.get_all_groups(),
            state=self.RegisterChangeGroupFSM.waiting_for_new_group,
        )

        dp.register_message_handler(
            self.set_edited_fio, state=self.RegisterChangeFioFSM.waiting_for_new_fio
        )

        dp.register_message_handler(
            self.not_registered,
            lambda message: self.notRegisteredExceptions(user_id=message.chat.id),
        )

        dp.register_callback_query_handler(
            self.register_change_true, text="register_change_true"
        )

        dp.register_callback_query_handler(
            self.register_change_false, text="register_change_false"
        )

        dp.register_callback_query_handler(
            self.ask_edited_fio, text="register_change_fio"
        )

        dp.register_callback_query_handler(
            self.ask_edited_group, text="register_change_group"
        )
