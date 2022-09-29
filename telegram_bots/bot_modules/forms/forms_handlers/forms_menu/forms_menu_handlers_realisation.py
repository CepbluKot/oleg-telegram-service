from operator import itemgetter
from aiogram import Dispatcher, types
from bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_interface import (
    FormsMenuHandlersInterface,
)


from bots import prepod_bot
from bot_modules.register.input_output_repositories import (
    currently_changing_register_data_repository_abs,
)
from bot_modules.forms.input_output_repositories import (
    choosing_groups_dispatcher_abs,
    forms_repository_abs,
    currently_editing_form_repository_abs,
)
from bot_modules.service_info.input_output_repositories import groups_repository_abs
from bot_modules.forms.input_output_realisations import (
    forms_constructor_abs,
    forms_editor_abs,
    forms_menu_abs,
)


class FormsMenuHandlersRealisation(FormsMenuHandlersInterface):
    async def choose_groups(self, message: types.Message):
        """Спрашивает юзера"""
        form_index = message.text[6:]
        if str(message.chat.id) == forms_menu_abs.get_form_creator_id(
            form_id=int(form_index)
        ):
            all_groups = groups_repository_abs.get_related_to_prepod_groups(
                user_id=message.chat.id
            )

            sent_polls = await forms_menu_abs.send_big_poll(
                user_id=message.chat.id, poll_options=all_groups
            )
            choosing_groups_dispatcher_abs.add_user(
                user_id=message.chat.id,
                polls=sent_polls,
                selected_form=forms_repository_abs.get_form(form_id=form_index),
            )

        else:
            await message.answer("Вы не являетесь создателем формы")

    async def display_forms_repository(self, message: types.message):
        await forms_editor_abs.display_forms_repository(user_id=message.chat.id)

    def lambda_checker_poll(self, poll_answer: types.PollAnswer):
        """Проверяет опрос"""
        return choosing_groups_dispatcher_abs.poll_checker(poll_answer=poll_answer)

    async def poll_handler(self, poll_answer: types.PollAnswer):
        """Активируется, когда приходит ответ на опрос/ опрос закрывается"""
        polls_data = choosing_groups_dispatcher_abs.get_user_polls(
            user_id=poll_answer.user.id
        )

        for selected_poll in polls_data:
            if selected_poll.poll_id == poll_answer.poll_id:

                selected_groups = itemgetter(*poll_answer.option_ids)(
                    selected_poll.poll_options
                )

                if "Ни одна из вышеперечисленных" not in selected_groups:
                    choosing_groups_dispatcher_abs.add_selected_groups(
                        user_id=poll_answer.user.id, groups=selected_groups
                    )

                polls_data.remove(selected_poll)

        if not polls_data:
            all_selected_groups = choosing_groups_dispatcher_abs.get_selected_groups(
                user_id=poll_answer.user.id
            )

            forms_menu_abs.send_form(
                form=choosing_groups_dispatcher_abs.get_selected_form(
                    user_id=poll_answer.user.id
                ),
                send_to_groups=all_selected_groups,
            )
            choosing_groups_dispatcher_abs.remove_user(user_id=poll_answer.user.id)

            # notifications_abs ...

            await prepod_bot.send_message(
                text="Отправлено группам " + "".join(str(all_selected_groups)),
                reply_markup=types.ReplyKeyboardRemove(),
                chat_id=poll_answer.user.id,
            )

    def saved_forms_exceptions(self, user_id: int):
        return (
            not forms_constructor_abs.check_is_user_is_creating_form(user_id=user_id)
            and not currently_changing_register_data_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
            and not choosing_groups_dispatcher_abs.is_user_in_list(user_id=user_id)
            and not currently_editing_form_repository_abs.check_is_user_in_list(
                user_id=user_id
            )
        )

    def forms_menu_handlers_registrator(self, dp: Dispatcher):
        dp.register_message_handler(
            self.display_forms_repository,
            lambda message: self.saved_forms_exceptions(user_id=message.chat.id),
            commands="saved_forms",
        )
        dp.register_message_handler(
            self.choose_groups, lambda message: message.text.startswith("/send")
        )
        dp.register_poll_answer_handler(
            self.poll_handler, lambda message: self.lambda_checker_poll(message)
        )
