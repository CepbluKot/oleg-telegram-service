""" Система регистарции пользователей"""
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from bots_setting.bot_elements.getters.register_getters import register_data_check_is_registered, register_data_get_phone_number, register_data_get_user_name
from bots_setting.bot_elements.setters.register_setters import register_data_add_user, register_data_change_phone_number, register_data_change_user_name


class register_user(StatesGroup):
    " FSM для регистрации пользователя"
    input_user_name = State()
    waiting_for_user_name = State()
    waiting_for_phone_number = State()


class register_change_phone_number_fsm(StatesGroup):
    " FSM для смены группы пользователя"
    waiting_for_new_phone_number = State()


class register_change_user_name_fsm(StatesGroup):
    " FSM для смены имени пользователя"
    waiting_for_new_user_name = State()


async def already_registered(message: types.Message, state: FSMContext):
    " Проверяет, зарегистрирован ли пользователь"
        
    await message.answer('Вы уже зарегистрированы: ' + '\nВы: ' + str(register_data_get_user_name(user_id=message.chat.id)) + '; ' + 'Ваш номер телефона: ' + str(register_data_get_phone_number(user_id=message.chat.id)), reply_markup=types.ReplyKeyboardRemove())
    
    buttons = [
        types.InlineKeyboardButton(
            text="Да", callback_data="register_change_true"),
        types.InlineKeyboardButton(
            text="Нет", callback_data="register_change_false")
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await message.answer('Хотите изменить рег. данные?', reply_markup=keyboard)


async def get_user_name(message: types.Message, state: FSMContext):
    " (register_user FSM) Ждем ввода имени"
    await message.answer("Введите ваше имя")
    await register_user.waiting_for_user_name.set()


async def get_phone_number(message: types.Message, state: FSMContext):
    " (register_user FSM) Получаем имя и предлагаем вести номер телефона"
    user_name = message.text
    await state.update_data(user_name=user_name)
    await message.reply('Введите ваш номер телефона')
    await register_user.waiting_for_phone_number.set()


# async def wrong_phone_number(message: types.Message):
#     " (register_user FSM) Срабатывает, если найдена ошибка в формате номера"
#     return await message.reply('Пожалуйста, введите номер телефона в правильном формате')


async def save_to_storage(message: types.Message, state: FSMContext):
    " (register_user FSM) Получаем номер телефона и добавляем пользователя в хранилище"
    user_data = await state.get_data()
    phone_number = message.text
    await message.answer( 'Вы зарегистрированы' + '\nВаше имя: ' + user_data['user_name'] + '; Ваш номер телефона: ' + phone_number, reply_markup=types.ReplyKeyboardRemove())
    await register_data_add_user(user_id=message.chat.id, user_name=user_data['user_name'], phone_number=phone_number)
    await state.finish()


async def register_change_true(call: types.CallbackQuery, state: FSMContext):
    " (already_registered Func) Выбираем какие рег. данные изменить"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)

    buttons = [
        types.InlineKeyboardButton(
            text="Имя", callback_data="register_change_user_name"),
        types.InlineKeyboardButton(
            text="Номер телефона", callback_data="register_change_phone_number")
    ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    await call.message.answer('Что именно изменить?', reply_markup=keyboard)


async def register_change_false(call: types.CallbackQuery, state: FSMContext):
    " (already_registered Func) Не меняем рег. данные"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await call.message.answer('Окес, ничего не меняем')


async def register_change_user_name(call: types.CallbackQuery, state: FSMContext):
    " (register_change_true Func) Предлагаем ввести новое имя"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await register_change_user_name_fsm.waiting_for_new_user_name.set()
    await call.message.answer('Введите новое имя')


async def register_change_phone_number(call: types.CallbackQuery, state: FSMContext):
    " (register_change_true Func) Предлагаем ввести новый номер телефона"
    await call.answer()
    await types.Message.edit_reply_markup(self=call.message, reply_markup=None)
    await register_change_phone_number_fsm.waiting_for_new_phone_number.set()
    await call.message.answer('Введите новый номер телефона')


# register_change_user_name_fsm.waiting_for_new_user_name
async def register_change_user_name_set(message: types.Message, state: FSMContext):
    " (register_change_user_name_fsm FSM) Получаем новое имя и обновляем данные"
    new_user_name = message.text
    register_data_change_user_name(user_id=message.chat.id, new_user_name=new_user_name)
    await message.reply(' Рег. данные обновлены, ваши текущие данные:\n' + ' Ваше имя: ' + register_data_get_user_name(message.chat.id) + '; Ваш номер телефона:' + register_data_get_phone_number(message.chat.id))
    await state.finish()

   
# register_change_phone_number_fsm.waiting_for_new_phone_number
async def register_change_phone_number_set(message: types.Message, state: FSMContext):
    " (register_change_group_fsm FSM) Получаем новую группу и обновляем данные"
    new_phone_number = message.text
    register_data_change_phone_number(user_id=message.chat.id, new_phone_number=new_phone_number)
    await message.reply('Рег. данные обновлены, ваши текущие данные:\n' + ' Ваше имя: ' + register_data_get_user_name(message.chat.id) + '; Ваш номер телефона:' + register_data_get_phone_number(message.chat.id))
    await state.finish()


def register_handler_register_user(dp: Dispatcher):
    dp.register_message_handler(
        already_registered, lambda message: register_data_check_is_registered(message.chat.id), commands='register')
    
    dp.register_message_handler(get_user_name, commands="register", state="*")
    dp.register_message_handler(get_phone_number, state=register_user.waiting_for_user_name)
    dp.register_message_handler(
        save_to_storage, state=register_user.waiting_for_phone_number)

    dp.register_message_handler(
        register_change_user_name_set, state=register_change_user_name_fsm.waiting_for_new_user_name)
    dp.register_message_handler(
        register_change_phone_number_set, state=register_change_phone_number_fsm.waiting_for_new_phone_number)

    dp.register_callback_query_handler(
        register_change_true, text="register_change_true")
    dp.register_callback_query_handler(
        register_change_false, text="register_change_false")
    dp.register_callback_query_handler(
        register_change_user_name, text="register_change_user_name")
    dp.register_callback_query_handler(
        register_change_phone_number, text="register_change_phone_number")
