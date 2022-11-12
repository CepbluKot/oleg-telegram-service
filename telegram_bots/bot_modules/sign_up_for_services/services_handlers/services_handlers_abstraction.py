from bot_modules.sign_up_for_services.services_handlers.services_handlers_interface import (
    ChooseServiceInterface,
)
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


class ChooseServiceHandlersAbstraction(ChooseServiceInterface):
    def __init__(self, interface: ChooseServiceInterface) -> None:
        self.interface = interface

    async def choose_service_name(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем имя услуги"
        return self.interface.choose_service_name(message=message, state=state)

    async def choose_service_week(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем неделю предоставления услуги"
        return self.interface.choose_service_week(message=message, state=state)

    async def choose_service_day(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем день предоставления услуги"
        return self.interface.choose_service_day(message=message, state=state)

    async def choose_service_final(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) генерируем окончательную инфу об услуге"
        return self.interface.choose_service_final(message=message, state=state)

    def services_handlers_registrator(self, dp: Dispatcher):
        return self.interface.services_handlers_registrator(dp=dp)

    
    def choose_service_name_checker(self, message: types.Message):
        return self.interface.choose_service_name_checker(message)
    
    def choose_service_week_checker(self, message: types.Message):
        return self.interface.choose_service_week_checker(message)

    def choose_service_day_checker(self, message: types.Message):
        return self.interface.choose_service_day_checker(message)
    
    async def choose_service_name_error(self, message: types.Message):
        return self.interface.choose_service_name_error(message)

    async def choose_service_week_error(self, message: types.Message):
        return self.interface.choose_service_week_error(message)

    async def choose_service_day_error(self, message: types.Message):
        return self.interface.choose_service_day_error(message)
