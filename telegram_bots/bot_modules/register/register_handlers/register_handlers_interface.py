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


class CustomersHandlersInterface(ABC):
    @abstractmethod
    async def already_registered(self, message: types.Message, state: FSMContext):
        " Проверяет, зарегистрирован ли пользователь"
        raise NotImplemented

    @abstractmethod
    async def get_user_name(self, message: types.Message, state: FSMContext):
        " (register_user FSM) Ждем ввода имени"
        raise NotImplemented

    @abstractmethod
    async def get_phone_number(self, message: types.Message, state: FSMContext):
        " (register_user FSM) Получаем имя и предлагаем вести номер телефона"
        raise NotImplemented

    @abstractmethod
    async def save_to_storage(self, message: types.Message, state: FSMContext):
        " (register_user FSM) Получаем номер телефона и добавляем пользователя в хранилище"
        raise NotImplemented

    @abstractmethod
    async def register_change_true(self, call: types.CallbackQuery, state: FSMContext):
        " (already_registered Func) Выбираем какие рег. данные изменить"
        raise NotImplemented

    @abstractmethod
    async def register_change_false(self, call: types.CallbackQuery, state: FSMContext):
        " (already_registered Func) Не меняем рег. данные"
        raise NotImplemented

    @abstractmethod
    async def register_change_user_name(self, call: types.CallbackQuery, state: FSMContext):
        " (register_change_true Func) Предлагаем ввести новое имя"
        raise NotImplemented

    @abstractmethod
    async def register_change_phone_number(self, call: types.CallbackQuery, state: FSMContext):
        " (register_change_true Func) Предлагаем ввести новый номер телефона"
        raise NotImplemented

    @abstractmethod
    async def register_change_user_name_set(self, message: types.Message, state: FSMContext):
        " (register_change_user_name_fsm FSM) Получаем новое имя и обновляем данные"
        raise NotImplemented

    @abstractmethod
    async def register_change_phone_number_set(self, message: types.Message, state: FSMContext):
        " (register_change_group_fsm FSM) Получаем новую группу и обновляем данные"
        raise NotImplemented

    @abstractmethod
    def register_handlers_registrator(self, dp: Dispatcher):
        raise NotImplemented
