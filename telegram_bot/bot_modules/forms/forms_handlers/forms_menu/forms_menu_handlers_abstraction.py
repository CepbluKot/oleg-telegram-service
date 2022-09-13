from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_interface import (
    FormsMenuHandlersInterface,
)


class FormsMenuHandlersAbstraction(FormsMenuHandlersInterface):
    def __init__(self, interface: FormsMenuHandlersInterface) -> None:
        self.interface = interface

    async def choose_groups(self, message: types.Message, state: FSMContext):
        """Спрашивает юзера"""
        return self.interface.choose_groups(message=message, state=state)

    async def display_forms_repository(self, message: types.message):
        return self.interface.display_forms_repository(message=message)

    def lambda_checker_poll(self, pollAnswer: types.PollAnswer):
        """Проверяет опрос"""
        return self.interface.lambda_checker_poll(poll_answer=pollAnswer)

    async def poll_handler(self, pollAnswer: types.PollAnswer):
        """Активируется, когда приходит ответ на опрос/ опрос закрывается"""
        return self.interface.poll_handler(poll_answer=pollAnswer)

    def forms_menu_handlers_registrator(self, dp: Dispatcher):
        return self.interface.forms_menu_handlers_registrator(dp=dp)
