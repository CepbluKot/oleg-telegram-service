""" Статус пользователя"""
import asyncio
from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
from bots import student_bot
import collections
from bot_modules.special_functions.functions_for_text_interface import (
    prepod_delete_previous_messages,
    student_delete_previous_messages,
    student_delete_previous_polls,
)
from bot_modules.user_interface.ui_handlers.ui_handlers_interface import (
    PrepodHandlersStatusInterface,
    StudentHandlersStatusInterface,
)


from bot_modules.forms.input_output_repositories import sent_forms_repository_abs
from bot_modules.user_interface.input_output_repositories import (
    completing_forms_dispatcher_abs,
    ui_repostiory_abs,
)
from bot_modules.register.input_output_realisations import register_for_university_abs
from bot_modules.settings.input_output_repositories import settings_repository_abs


class PrepodHandlersStatus(PrepodHandlersStatusInterface):
    async def choose_ui_type(self, message: types.Message):
        settings_repository_abs.add_user(user_id=message.chat.id)
        buttons = [
            types.InlineKeyboardButton(text="GUI", callback_data="ui_type_gui"),
            types.InlineKeyboardButton(text="Текст", callback_data="ui_type_text"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(
            "Выберите тип пользовательского интерфейса", reply_markup=keyboard
        )

    async def set_ui_type_gui(self, call: types.CallbackQuery):
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        ui_repostiory_abs.set_users_ui_to_gui(user_id=call.from_user.id)
        answer = await call.message.reply(
            "Выбран графический интерфейс, для взаимодействия пользуйтесь приложением",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="Приложение", web_app=WebAppInfo(url="https://chromedino.com/")
                )
            ),
        )

        await prepod_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def set_ui_type_text(self, call: types.CallbackQuery):
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        ui_repostiory_abs.set_users_ui_to_text(user_id=call.from_user.id)
        answer = await call.message.reply(
            "Выбран текстовый интерфейс, для взаимодействия пользуйтесь командами"
        )

        await prepod_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def display_user_status(self, message: types.Message):
        full_message = "Отправленные вами формы:"
        sent_forms_mem = sent_forms_repository_abs.get_forms_sent_by_user(
            user_id=message.chat.id
        )
        for form in sent_forms_mem:
            if len(form.sent_to_users_ids) != 0:
                full_message += (
                    "\n"
                    + "НАЗВАНИЕ: "
                    + str(form.form_name)
                    + " ПРОЦЕСС ВЫПОЛНЕНИЯ: "
                    + str(
                        len(form.completed_users_ids)
                        / len(form.sent_to_users_ids)
                        * 100
                    )
                    + " % ("
                    + str(len(form.completed_users_ids))
                    + " / "
                    + str(len(form.sent_to_users_ids))
                    + ") /getResult_"
                    + str(form.form_id)
                    + "_"
                    + str(form.sent_form_id)
                )

            else:
                full_message += (
                    "\n"
                    + "НАЗВАНИЕ: "
                    + str(form.form_name)
                    + " ПРОЦЕСС ВЫПОЛНЕНИЯ: "
                    + "0 % ("
                    + str(len(form.completed_users_ids))
                    + " / "
                    + str(len(form.sent_to_users_ids))
                    + ") /getResult_"
                    + str(form.form_id)
                    + "_"
                    + str(form.sent_form_id)
                )

        if not len(sent_forms_mem):
            await message.answer("Вы не создали ни одной формы")

        else:
            await message.answer(full_message)

    def get_form_result(self, message: types.Message):
        pass

    async def wrong_interface(self, message: types.Message):

        answer = await message.answer(
            "Используйте графический интерфейс",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="Приложение", web_app=WebAppInfo(url="https://chromedino.com/")
                )
            ),
        )

        await prepod_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=1
        )

    def wrong_interface_exceptions(self, message: types.Message):
        result = ui_repostiory_abs.get_users_ui(user_id=message.chat.id)
        if result:
            return result.GUI
        else:
            return False

    async def interface_not_selected(self, message: types.Message):
        answer = await message.answer("Выберите интерфейс - /start")

        await prepod_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=1
        )

    def interface_not_selected_exceptions(self, message: types.Message):
        return not ui_repostiory_abs.check_is_user_selected_ui(user_id=message.chat.id)

    def status_exceptions(self, message: types.Message):
        return register_for_university_abs.check_is_user_in_register_data(user_id=message.chat.id)

    def register_handlers_prepod_status(self, dp: Dispatcher):
        dp.register_message_handler(self.choose_ui_type, commands="start")
        dp.register_message_handler(
            self.interface_not_selected,
            lambda message: self.interface_not_selected_exceptions(message=message),
        )
        dp.register_message_handler(
            self.wrong_interface,
            lambda message: self.wrong_interface_exceptions(message=message),
        )
        dp.register_message_handler(
            self.display_user_status,
            lambda message: self.status_exceptions(message=message),
            commands="status",
        )
        dp.register_message_handler(
            self.get_form_result, lambda message: message.text.startswith("/getResult_")
        )

        dp.register_callback_query_handler(self.set_ui_type_gui, text="ui_type_gui")

        dp.register_callback_query_handler(self.set_ui_type_text, text="ui_type_text")


class StudentHandlersStatus(StudentHandlersStatusInterface):
    async def choose_ui_type(self, message: types.Message):
        settings_repository_abs.add_user(user_id=message.chat.id)
        buttons = [
            types.InlineKeyboardButton(text="GUI", callback_data="ui_type_gui"),
            types.InlineKeyboardButton(text="Текст", callback_data="ui_type_text"),
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await message.answer(
            "Выберите тип пользовательского интерфейса", reply_markup=keyboard
        )

    async def set_ui_type_gui(self, call: types.CallbackQuery):
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        ui_repostiory_abs.set_users_ui_to_gui(user_id=call.from_user.id)
        answer = await call.message.reply(
            "Выбран графический интерфейс, для взаимодействия пользуйтесь приложением",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="Приложение", web_app=WebAppInfo(url="https://chromedino.com/")
                )
            ),
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def set_ui_type_text(self, call: types.CallbackQuery):
        await call.answer()
        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        ui_repostiory_abs.set_users_ui_to_text(user_id=call.from_user.id)
        answer = await call.message.reply(
            "Выбран текстовый интерфейс, для взаимодействия пользуйтесь командами"
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def display_user_status(self, message: types.Message):
        full_message = "Полученные формы:"
        recieved_forms = sent_forms_repository_abs.get_recieved_forms(
            user_id=message.chat.id
        )
        for form in recieved_forms:
            if (
                str(message.chat.id) in form.sent_to_users_ids
                and not str(message.chat.id) in form.completed_users_ids
            ):
                full_message += (
                    "\n"
                    + str(form.form_name)
                    + " от пользователя "
                    + str(form.creator.fio)
                    + " /complete_"
                    + str(form.form_id)
                    + "_"
                    + str(form.sent_form_id)
                )

        if not len(recieved_forms):
            full_message = "Нет полученных форм"

        full_message += "\n "

        answer = await message.answer(full_message)

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=2
        )

    async def complete_form(self, message: types.Message):
        """Получает название формы, добавляет данные в forms_dispatcher,
        запускает отправку вопросов из нужной формы"""

        form_indexes = message.text[10:].split("_")
        unique_sent_form_id = int(form_indexes[1])

        sent_form = sent_forms_repository_abs.get_form(sent_form_id=unique_sent_form_id)
        completing_forms_dispatcher_abs.add_user(
            user_id=message.chat.id, sent_form=sent_form
        )

        await self.go_cycle(message=message, type="launch_from_message_handler")
        await student_delete_previous_messages(
            last_message_to_delete=message, num_of_messages_to_delete=1, timer=False
        )

    async def go_cycle(self, message, type: str):
        """Отсылает вопросы/ опросы из completing_forms_dispatcher при вызове"""
        user_id = 0
        if type == "launch_from_poll_handler":
            user_id = message.user.id

        elif type == "launch_from_message_handler":
            user_id = message.chat.id

        dispatcher_data = completing_forms_dispatcher_abs.get_dispatcher_data(
            user_id=user_id
        )

        if dispatcher_data.current_question_num == len(
            dispatcher_data.current_sent_form.questions
        ):

            buttons = [
                types.InlineKeyboardButton(
                    text="Отправить ответы на форму", callback_data="send_form_answers"
                ),
            ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            await student_bot.send_message(
                chat_id=user_id,
                text="Форма пройдена, вы можете исправить ответы, по окончании нажмите на кнопку отправки формы",
                reply_markup=keyboard,
            )

        elif dispatcher_data.current_question.question_type == "poll":
            msg = await student_bot.send_poll(
                chat_id=user_id,
                question=dispatcher_data.current_question.question_text,
                options=dispatcher_data.current_question.options,
                is_anonymous=False,
            )
            completing_forms_dispatcher_abs.set_current_question_message_id(
                user_id=user_id, message_id=msg.poll.id
            )

        elif dispatcher_data.current_question.question_type == "msg":
            msg = await student_bot.send_message(
                chat_id=user_id, text=dispatcher_data.current_question.question_text
            )
            completing_forms_dispatcher_abs.set_current_question_message_id(
                user_id=user_id, message_id=msg.message_id
            )
            print(msg.message_id)

    async def form_edit_handler(self, message: types.Message):
        completing_forms_dispatcher_abs.update_question_answer(
            user_id=message.chat.id,
            question_message_id=message.message_id,
            new_answer=message.text,
        )
        print("saved")

    async def form_completed(self, call: types.CallbackQuery):
        await call.answer()

        completed_form_sent_form_id = (
            completing_forms_dispatcher_abs.get_dispatcher_data(
                user_id=call.from_user.id
            ).current_sent_form.sent_form_id
        )
        completing_forms_dispatcher_abs.delete_user(user_id=call.from_user.id)

        sent_forms_repository_abs.add_completed_user(
            sent_form_id=completed_form_sent_form_id, user_id=call.from_user.id
        )
        completed_form_data = sent_forms_repository_abs.get_form(
            sent_form_id=completed_form_sent_form_id
        )

        if collections.Counter(
            completed_form_data.completed_users_ids
        ) == collections.Counter(completed_form_data.sent_to_users_ids):
            print("FORM FULLY COMPLETED")

        await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
        await call.message.reply("форма отправлена")

    def lambda_checker_poll(self, poll_answer: types.PollAnswer):
        """Проверяет принадлежит ли опрос выбранной форме"""
        dispatcher_data = completing_forms_dispatcher_abs.get_dispatcher_data(
            user_id=poll_answer.user.id
        )
        if str(dispatcher_data.current_question.question_message_id) == str(
            poll_answer.poll_id
        ):
            dispatcher_data.current_question.user_answered = poll_answer.option_ids

            completing_forms_dispatcher_abs.set_next_question(
                user_id=poll_answer.user.id
            )

            return True

        return False

    def lambda_checker_msg(self, message_answer: types.Message):
        """Проверяет является ли сообщение ответом на вопрос из формы"""
        dispatcher_data = completing_forms_dispatcher_abs.get_dispatcher_data(
            user_id=message_answer.from_user.id
        )
        if str(dispatcher_data.current_question.question_message_id) == str(
            message_answer.message_id - 1
        ):
            dispatcher_data.current_question.user_answered = message_answer.text

            completing_forms_dispatcher_abs.set_next_question(
                user_id=message_answer.from_user.id
            )

            return True

        return False

    async def poll_handler(self, poll_answer: types.PollAnswer):
        """Активируется, когда приходит ответ на опрос/ опрос закрывается"""
        await self.go_cycle(message=poll_answer, type="launch_from_poll_handler")
        # await student_delete_previous_polls(
        #     last_message_to_delete=poll_answer, num_of_messages_to_delete=2
        # )

    async def msg_handler(self, message_answer: types.Message):
        """Активируется, когда приходит сообщение"""
        await self.go_cycle(message=message_answer, type="launch_from_message_handler")
        # await student_delete_previous_messages(
        #     last_message_to_delete=message_answer, num_of_messages_to_delete=2
        # )

    def check_is_already_completed(self, message: types.Message):
        form_indexes = message.text[10:].split("_")

        unique_sent_form_id = int(form_indexes[1])

        if (
            message.chat.id
            in sent_forms_repository_abs.get_form(
                sent_form_id=unique_sent_form_id
            ).completed_users_ids
        ):
            return True
        return False

    async def already_completed_message_reply(self, message: types.Message):
        await message.answer("Вы уже прошли данную форму")

        await student_delete_previous_messages(
            last_message_to_delete=message, num_of_messages_to_delete=1
        )

    async def wrong_interface(self, message: types.Message):
        answer = await message.answer(
            "Используйте графический интерфейс",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton(
                    text="Приложение", web_app=WebAppInfo(url="https://chromedino.com/")
                )
            ),
        )

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=1
        )

    def wrong_interface_exceptions(self, message: types.Message):
        result = ui_repostiory_abs.get_users_ui(user_id=message.chat.id)
        if result:
            return result.GUI
        return False

    async def interface_not_selected(self, message: types.Message):
        answer = await message.answer("Выберите интерфейс - /start")

        await student_delete_previous_messages(
            last_message_to_delete=answer, num_of_messages_to_delete=1
        )

    def interface_not_selected_exceptions(self, message: types.Message):
        return not ui_repostiory_abs.check_is_user_selected_ui(user_id=message.chat.id)

    def status_exceptions(self, message: types.Message):
        return register_for_university_abs.check_is_user_in_register_data(user_id=message.chat.id)

    def register_handlers_student_status(self, dp: Dispatcher):
        dp.register_message_handler(self.choose_ui_type, commands="start")
        dp.register_message_handler(
            self.interface_not_selected,
            lambda message: self.interface_not_selected_exceptions(message=message),
        )
        dp.register_message_handler(
            self.wrong_interface,
            lambda message: self.wrong_interface_exceptions(message=message),
        )
        dp.register_message_handler(
            self.display_user_status,
            lambda message: self.status_exceptions(message=message),
            commands="status",
        )
        dp.register_message_handler(
            self.already_completed_message_reply,
            lambda message: message.text.startswith("/complete")
            and self.check_is_already_completed(message),
        )
        dp.register_message_handler(
            self.complete_form, lambda message: message.text.startswith("/complete")
        )
        dp.register_poll_answer_handler(
            self.poll_handler,
            lambda message: completing_forms_dispatcher_abs.check_is_user_completing_form(
                user_id=message.user.id
            )
            and self.lambda_checker_poll(message),
        )
        dp.register_message_handler(
            self.msg_handler,
            lambda message: completing_forms_dispatcher_abs.check_is_user_completing_form(
                user_id=message.from_user.id
            )
            and self.lambda_checker_msg(message),
        )

        dp.register_edited_message_handler(self.form_edit_handler)

        dp.register_callback_query_handler(self.set_ui_type_gui, text="ui_type_gui")

        dp.register_callback_query_handler(self.set_ui_type_text, text="ui_type_text")

        dp.register_callback_query_handler(
            self.form_completed, text="send_form_answers"
        )
