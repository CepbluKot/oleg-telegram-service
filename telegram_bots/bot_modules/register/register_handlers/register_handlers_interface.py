from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from abc import abstractmethod, ABC


class BaseRegisterHandlersInterface(ABC):
    @abstractmethod
    async def not_confirmed(self, message: types.Message):
        raise NotImplementedError

    @abstractmethod
    async def already_registered(self, message: types.Message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def ask_register_fio(self, message: types.message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def register_fio_chosen(self, message: types.Message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def register_change_true(self, call: types.CallbackQuery, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def register_change_false(self, call: types.CallbackQuery, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def ask_edited_fio(self, message: types.Message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def set_edited_fio(self, message: types.Message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def not_registered(self, message: types.Message):
        raise NotImplemented


class PrepodHandlersInterface(BaseRegisterHandlersInterface):
    @abstractmethod
    def prepod_registration_handlers_registrator(self, dp: Dispatcher):
        raise NotImplementedError


class StudentHandlersInterface(BaseRegisterHandlersInterface):
    @abstractmethod
    async def wrong_group(self, message: types.Message):
        raise NotImplementedError

    @abstractmethod
    async def register_group_chosen(self, message: types.Message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def ask_edited_group(self, message: types.Message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    async def set_edited_group(self, message: types.Message, state: FSMContext):
        raise NotImplementedError

    @abstractmethod
    def student_registration_handlers_register(self, dp: Dispatcher):
        raise NotImplementedError
