from bot_modules.user_interface.ui_handlers.ui_handlers_interface import (
    PrepodHandlersStatusInterface,
    StudentHandlersStatusInterface,
)
from aiogram import types, Dispatcher


class PrepodHandlersStatusAbstraction(PrepodHandlersStatusInterface):
    def __init__(self, interface: PrepodHandlersStatusInterface) -> None:
        self.interface = interface

    async def choose_ui_type(self, message: types.Message):
        return self.interface.choose_ui_type(message=message)

    async def set_ui_type_gui(self, call: types.CallbackQuery):
        return self.interface.set_ui_type_gui(call=call)

    async def set_ui_type_text(self, call: types.CallbackQuery):
        return self.interface.set_ui_type_text(call=call)

    async def display_user_status(self, message: types.Message):
        return self.interface.display_user_status(message=message)

    def get_form_result(self, message: types.Message):
        return self.interface.get_form_result(message=message)

    def register_handlers_prepod_status(self, dp: Dispatcher):
        return self.interface.register_handlers_prepod_status(dp=dp)


class StudentHandlersStatusAbstraction(StudentHandlersStatusInterface):
    def __init__(self, interface: StudentHandlersStatusInterface) -> None:
        self.interface = interface

    async def choose_ui_type(self, message: types.Message):
        return self.interface.choose_ui_type(message=message)

    async def set_ui_type_gui(self, call: types.CallbackQuery):
        return self.interface.set_ui_type_gui(call=call)

    async def set_ui_type_text(self, call: types.CallbackQuery):
        return self.interface.set_ui_type_text(call=call)

    async def display_user_status(self, message: types.Message):
        return self.interface.display_user_status(message=message)

    async def complete_form(self, message: types.Message):
        """Получает название формы, добавляет данные в forms_dispatcher,
        запускает отправку вопросов из нужной формы"""
        return self.interface.complete_form(message=message)

    async def go_cycle(self, message, type):
        """Отсылает вопросы/ опросы из completing_forms_dispatcher при вызове"""
        return self.interface.go_cycle(message=message)

    def lambda_checker_poll(self, pollAnswer: types.PollAnswer):
        """Проверяет принадлежит ли опрос выбранной форме"""
        return self.interface.lambda_checker_poll(poll_answer=pollAnswer)

    def lambda_checker_msg(self, message: types.Message):
        """Проверяет является ли сообщение ответом на вопрос из формы"""
        return self.interface.lambda_checker_msg(message=message)

    async def poll_handler(self, pollAnswer: types.PollAnswer):
        """Активируется, когда приходит ответ на опрос/ опрос закрывается"""
        return self.interface.poll_handler(poll_answer=pollAnswer)

    async def msg_handler(self, message: types.Message):
        """Активируется, когда приходит сообщение"""
        return self.interface.msg_handler(message=message)

    def check_is_already_completed(self, message: types.Message):
        return self.interface.check_is_already_completed(message=message)

    async def already_completed_message_reply(self, message: types.Message):
        return self.interface.already_completed_message_reply(message=message)

    def register_handlers_student_status(self, dp: Dispatcher):
        return self.interface.register_handlers_student_status(dp=dp)
