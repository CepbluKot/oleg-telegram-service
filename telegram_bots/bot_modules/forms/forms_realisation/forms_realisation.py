from bot_modules.forms.forms_realisation.forms_realisation_interface import (
    FormsConstructorInterface,
    FormsEditorInterface,
    FormsMenuInterface,
    FormsSenderInterface,
)
from typing import List
from aiogram import types

from bots import prepod_bot
from bot_modules.forms.data_structures import (
    ChoosingGroupsPoll,
    Form,
    SentForm,
    TextQuestion,
    PollQuestion,
    Question,
    User,
)

from bot_modules.register.input_output_repositories import register_repository_abs
from bot_modules.forms.input_output_repositories import (
    forms_constructor_repository_abs,
    forms_repository_abs,
    choosing_groups_dispatcher_abs,
    sent_forms_repository_abs,
)
from bot_modules.service_info.input_output_repositories import groups_repository_abs


class FormsConstructorRealisation(FormsConstructorInterface):
    def add_form(self, form: Form):
        forms_constructor_repository_abs.add_form(form=form)

    def add_text_question_to_form(self, text_question: TextQuestion, user_id: int):
        form = forms_constructor_repository_abs.get_form(user_id=user_id)
        form.questions.append(text_question)
        forms_constructor_repository_abs.update_form_data(form=form)

    def add_poll_question_to_form(self, poll_question: PollQuestion, user_id: int):
        form = forms_constructor_repository_abs.get_form(user_id=user_id)
        form.questions.append(poll_question)
        forms_constructor_repository_abs.update_form_data(form=form)

    async def display_form(self, user_id: int):
        """Выводит сообщением содержимое создаваемого опроса"""
        form = forms_constructor_repository_abs.get_form(user_id=user_id)

        parsed_msg = (
            "name: " + form.form_name + " " + "form.formId: " + str(form.form_id) + "\n"
        )
        if form.questions:
            question_number = 0
            for question in form.questions:
                if question.question_type == "poll":
                    parsed_msg += str(
                        question.question_type
                        + " "
                        + question.question_text
                        + " "
                        + "["
                        + ", ".join(str(e) for e in question.options)
                        + "]"
                        + " "
                        + "/del"
                        + str(question_number)
                        + "\n"
                    )

                elif question.question_type == "msg":
                    parsed_msg += str(
                        question.question_type
                        + " "
                        + question.question_text
                        + " "
                        + "/del"
                        + str(question_number)
                        + "\n"
                    )

                question_number += 1

            await prepod_bot.send_message(
                text=parsed_msg,
                reply_markup=types.ReplyKeyboardRemove(),
                chat_id=user_id,
            )

        else:
            await prepod_bot.send_message(
                text="vse ploho",
                reply_markup=types.ReplyKeyboardRemove(),
                chat_id=user_id,
            )

    def add_form_to_forms_repository(self, form: Form):
        forms_repository_abs.add_form(form=form)

    def generate_form_id(self) -> int:
        "generate form id"
        return forms_repository_abs.generate_form_id()

    def get_form(self, user_id: int) -> Form:
        return forms_constructor_repository_abs.get_form(user_id=user_id)

    def update_form_data(self, form: Form):
        forms_constructor_repository_abs.update_form_data(form=form)

    def check_is_user_is_creating_form(self, user_id: int):
        return forms_constructor_repository_abs.check_is_user_in_repository(
            user_id=user_id
        )

    def delete_question(self, question_id: str, user_id: int):
        form = forms_constructor_repository_abs.get_form(user_id=user_id)
        del form.questions[question_id]
        forms_constructor_repository_abs.update_form_data(form=form)

    def delete_form(self, user_id: int):
        forms_constructor_repository_abs.delete_form(user_id=user_id)


class FormsMenuRealisation(FormsMenuInterface):
    def add_user_to_choosing_groups_dispatcher(self, user_id: int):
        choosing_groups_dispatcher_abs.add_user(user_id=user_id)

    def add_selected_groups_to_choosing_groups_dispatcher(
        self, user_id: int, groups: List[str]
    ):
        choosing_groups_dispatcher_abs.add_selected_groups(
            user_id=user_id, groups=list(groups.copy())
        )

    def get_user_polls_from_choosing_groups_dispatcher(
        self, user_id: int
    ) -> List[ChoosingGroupsPoll]:
        return choosing_groups_dispatcher_abs.get_user_polls(user_id=user_id)

    def poll_checker_for_choosing_groups_dispatcher(
        self, poll_answer: types.PollAnswer
    ):
        return choosing_groups_dispatcher_abs.poll_checker(poll_answer=poll_answer)

    def get_selected_groups_from_choosing_groups_dispatcher(self, user_id: int):
        return choosing_groups_dispatcher_abs.get_selected_groups(user_id=user_id)

    def get_selected_form_from_choosing_groups_dispatcher(self, user_id: int) -> Form:
        return choosing_groups_dispatcher_abs.get_selected_form(user_id=user_id)

    def remove_user_from_choosing_groups_dispatcher(self, user_id: int):
        choosing_groups_dispatcher_abs.remove_user(user_id=user_id)

    def send_form(self, form: Form, send_to_groups: List[str]):
        sentForm = SentForm(
            form_id=form.form_id,
            form_name=form.form_name,
            creator=form.creator,
            questions=form.questions,
            sent_form_id=sent_forms_repository_abs.generate_sent_form_id(),
            sent_to_groups=send_to_groups,
            sent_to_users_ids=groups_repository_abs.get_students_ids_by_groups(
                send_to_groups
            ),
            completed_users_ids=[],
        )

        sent_forms_repository_abs.add_form(form=sentForm)
        print("very good")
        # add notify, etc...

    async def send_big_poll(self, user_id: int, poll_options: List[str]) -> List[str]:
        sent_polls = []
        index = 0
        creator_data: User = register_repository_abs.get_user_data(user_id=user_id)
        while len(poll_options):
            options = poll_options[:9]
            options.append("Ни одна из вышеперечисленных")
            poll = await prepod_bot.send_poll(
                chat_id=user_id,
                options=options,
                question="выберите группы для отпраки",
                is_anonymous=False,
                allows_multiple_answers=True,
            )

            data = ChoosingGroupsPoll(
                poll_id=poll.poll.id,
                poll_num=index,
                poll_options=options,
                created_by=creator_data,
            )

            sent_polls.append(data)
            poll_options = poll_options[9:]
            index += 1
        return sent_polls

    def get_form_creator_id(self, form_id: str):
        form = forms_repository_abs.get_form(form_id=form_id)
        return form.creator.user_id

    def get_groups_students_ids(self, groups: List[str]):
        return groups_repository_abs.get_students_ids_by_groups(groups=groups)


class FormsEditorRealisation(FormsEditorInterface):
    async def display_forms_repository(self, user_id: int):
        user_id = str(user_id)
        full_message = ""
        all_forms: List[Form] = forms_repository_abs.get_forms(user_id=user_id)

        if all_forms:
            for form in all_forms:
                parsed_msg = (
                    "\n ----- \nname: "
                    + form.form_name
                    + " "
                    + "formId: "
                    + str(form.form_id)
                    + " /send_"
                    + str(form.form_id)
                    + " /rename_"
                    + str(form.form_id)
                    + " /edit_"
                    + str(form.form_id)
                    + " /del_"
                    + str(form.form_id)
                    + "\n"
                )

                if form.questions:
                    for question in form.questions:
                        if question.question_type == "poll":
                            parsed_msg += str(
                                question.question_type
                                + " "
                                + question.question_text
                                + " "
                                + "["
                                + ", ".join(str(e) for e in question.options)
                                + "]"
                                + "\n"
                            )

                        elif question.question_type == "msg":
                            parsed_msg += str(
                                question.question_type
                                + " "
                                + question.question_text
                                + "\n"
                            )

                full_message += parsed_msg

            await prepod_bot.send_message(
                text=full_message, reply_markup=None, chat_id=user_id
            )

        else:
            await prepod_bot.send_message(
                text="Хранилище форм пусто", reply_markup=None, chat_id=user_id
            )

    async def display_form(self, form_id: str, user_id: int):
        user_id = str(user_id)
        form = forms_repository_abs.get_form(form_id=form_id)
        if user_id == str(form.creator.user_id):
            if form:
                parsed_msg = (
                    "name: "
                    + form.form_name
                    + " "
                    + "form.formId: "
                    + str(form.form_id)
                    + "\n"
                )
                if form:
                    question_number = 0
                    for question in form.questions:
                        if question.question_type == "poll":
                            parsed_msg += str(
                                question.question_type
                                + " "
                                + question.question_text
                                + " "
                                + "["
                                + ", ".join(str(e) for e in question.options)
                                + "]"
                                + " /rename"
                                + str(form.form_id)
                                + "_"
                                + str(question_number)
                                + " /add_after"
                                + str(form.form_id)
                                + "_"
                                + str(question_number)
                                + " /edit"
                                + str(form.form_id)
                                + "_"
                                + str(question_number)
                                + " /del"
                                + str(form.form_id)
                                + "_"
                                + str(question_number)
                                + "\n"
                            )

                        elif question.question_type == "msg":
                            parsed_msg += str(
                                question.question_type
                                + " "
                                + question.question_text
                                + " /rename"
                                + str(form.form_id)
                                + "_"
                                + str(question_number)
                                + " /add_after"
                                + str(form.form_id)
                                + "_"
                                + str(question_number)
                                + " /del"
                                + str(form.form_id)
                                + "_"
                                + str(question_number)
                                + "\n"
                            )

                        question_number += 1

                    await prepod_bot.send_message(
                        text=parsed_msg,
                        reply_markup=types.ReplyKeyboardRemove(),
                        chat_id=user_id,
                    )

            else:
                await prepod_bot.send_message(
                    text="Хранилище форм пусто",
                    reply_markup=types.ReplyKeyboardRemove(),
                    chat_id=user_id,
                )

        else:
            await prepod_bot.send_message(
                text="Вы не являетесь создателем формы",
                reply_markup=types.ReplyKeyboardRemove(),
                chat_id=user_id,
            )

    def set_new_form_name(self, form_id: str, new_name: str):
        form = forms_repository_abs.get_form(form_id=form_id)
        form.form_name = new_name
        forms_repository_abs.update_form_data(form=form.copy())

    def set_new_question_name(
        self, form_id: int, question_id: int, new_question_name: str
    ):
        form = forms_repository_abs.get_form(form_id=form_id)
        form.questions[question_id].question_text = new_question_name
        forms_repository_abs.update_form_data(form=form)

    def insert_question(self, form_id: int, insert_after_id: int, question: Question):
        form = forms_repository_abs.get_form(form_id=form_id)
        form.questions.insert(insert_after_id + 1, question)
        forms_repository_abs.update_form_data(form=form)

    def edit_poll_options(
        self, form_id: int, question_id: str, new_poll_options: List[str]
    ):
        form = forms_repository_abs.get_form(form_id=form_id)
        form.questions[question_id].options = new_poll_options
        forms_repository_abs.update_form_data(form=form)

    def delete_question(self, form_id: int, question_id: int):
        form = forms_repository_abs.get_form(form_id=form_id)
        del form.questions[question_id]

    def delete_form(self, form_id: int):
        forms_repository_abs.delete_form(form_id=form_id)


class FormsSenderRealisation(FormsSenderInterface):
    def get_forms_sent_by_user(self, user_id: int) -> List[SentForm]:
        return sent_forms_repository_abs.get_forms_sent_by_user(user_id=user_id)

    def add_sent_form(self, form: SentForm):
        sent_forms_repository_abs.add_form(form=form)

    def add_completed_user(self, sent_form_id: str, user_id: int):
        sent_forms_repository_abs.add_completed_user(
            sent_form_id=sent_form_id, user_id=user_id
        )

    def get_accepeted_forms(self, user_id: int) -> List[SentForm]:
        return sent_forms_repository_abs.get_recieved_forms(user_id=user_id)

    def get_form(self, sent_form_id: str):
        return sent_forms_repository_abs.get_form(sent_form_id=sent_form_id)

    def check_is_form_completed(self, sent_form_id: str):
        formData = sent_forms_repository_abs.get_form(sent_form_id=sent_form_id)
        if len(formData.completed_users_ids) == len(formData.sent_to_users_ids):
            return True

        return False
