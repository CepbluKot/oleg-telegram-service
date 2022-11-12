from abc import ABC, abstractmethod
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


class ChooseServiceInterface(ABC):
    @abstractmethod
    async def choose_service_name(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем имя услуги"
        raise NotImplemented

    @abstractmethod
    async def choose_service_week(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем неделю предоставления услуги"
        raise NotImplemented

    @abstractmethod
    async def choose_service_day(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) выбираем день предоставления услуги"
        raise NotImplemented

    @abstractmethod
    async def choose_service_final(self, message: types.Message, state: FSMContext):
        "(choose_service_fsm) генерируем окончательную инфу об услуге"
        raise NotImplemented

    @abstractmethod
    def services_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented

    @abstractmethod
    def choose_service_name_checker(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def choose_service_week_checker(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    def choose_service_day_checker(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def choose_service_name_error(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def choose_service_week_error(self, message: types.Message):
        raise NotImplemented

    @abstractmethod
    async def choose_service_day_error(self, message: types.Message):
        raise NotImplemented

