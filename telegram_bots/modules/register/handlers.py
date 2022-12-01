import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from telegram_bots.modules.register.repository.api_repository.output import register_repository_async, register_repository_sync
from telegram_bots.modules.register.repository.temporary_messages_repository.output import register_temporary_messages_repository
from telegram_bots.bots import bot
from telegram_bots.modules.register.data_structures import User
from telegram_bots.modules.register.repository.temporary_register_data.output import temporary_register_data


message_delete_delay = 5


class WaitForNameFSM(StatesGroup):
    wait_for_name = State()

class WaitForContactFSM(StatesGroup):
    wait_for_contact = State()


async def ask_for_name_input(message: types.Message):
    response = await register_repository_async.get_user(message.from_user.id)
    
    if response:
        if not response.errors.has_error:
            if response.data:
                if response.data.tg_id == message.chat.id:
                    await message.answer("Вы уже зарегистрированы")

            else:
                await message.answer("Как вас зовут?")
                await WaitForNameFSM.wait_for_name.set()
    
        else:
            if response.errors.timeout:
                await message.answer("В настоящий момент сервис не доступен, пожалуйста, повторите позже")
            
            else:
                await message.answer("Возникла непредвиденная ошибка")
    
    else:
        await message.answer("В настоящий момент сервис не доступен, пожалуйста, повторите позже")
            

async def ask_for_phone_number_input(message: types.Message, state: FSMContext):
    data = User(name=message.text, tg_id=message.chat.id)
    temporary_register_data.create(data)

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    buttons = [
            types.InlineKeyboardButton(
                text="Да", callback_data="enter_phone"),
            types.InlineKeyboardButton(
                text="Нет", callback_data="dont_enter_phone"),
        ]

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    await state.finish()
    await message.answer("Хотите ввести свой номер телефона?", reply_markup=keyboard)
    

async def enter_phone(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    send_phone_number_button = types.KeyboardButton(
        text="Отправить номер телефона", request_contact=True
    )
    keyboard.add(send_phone_number_button)
    msg = await call.message.answer(
        "Отправьтей свой контакт или введите номер телефона вручную", reply_markup=keyboard
    )

    register_temporary_messages_repository.append(msg)
    await WaitForContactFSM.wait_for_contact.set()


async def recieve_phone_number_contact(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    register_temporary_messages_repository.append(message)
    final_msg = await message.answer("Регистрация завершена", reply_markup=None)
    

    register_temporary_messages_repository.append(final_msg)
    # print('message.contact.phone_number', message.contact.phone_number, 'text', message.text)
    # do smth in api

    await state.finish()

    data = temporary_register_data.read(message.chat.id)
    data.phone = message.contact.phone_number

    await asyncio.sleep(message_delete_delay)
    for msg in register_temporary_messages_repository.read(final_msg.chat.id):
        await bot.delete_message(msg.chat.id, msg.message_id)

    register_temporary_messages_repository.delete(chat_id)


async def recieve_phone_number_text(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    register_temporary_messages_repository.append(message)
    final_msg = await message.answer("Регистрация завершена", reply_markup=None)

    register_temporary_messages_repository.append(final_msg)

    # print('message.contact.phone_number', message.contact.phone_number, 'text', message.text)
    # do smth in api
    await state.finish()

    data = temporary_register_data.read(message.chat.id)
    data.phone = message.text

    await asyncio.sleep(message_delete_delay)
    for msg in register_temporary_messages_repository.read(final_msg.chat.id):
        await bot.delete_message(msg.chat.id, msg.message_id)
    
    register_temporary_messages_repository.delete(chat_id)


def phone_number_check_contact(message: types.Message):
    data = temporary_register_data.read(message.chat.id)
    data.phone = message.contact.phone_number
    response = register_repository_sync.update_user(data)

    if response.errors.wrong_phone_number:
        return True


def phone_number_check_text(message: types.Message):
    data = temporary_register_data.read(message.chat.id)
    data.phone = message.text
    
    
    response = register_repository_sync.register_user(data)
    print('response',response.errors)
    if response.errors.wrong_phone_number:
        return True


async def wrong_phone_number_msg(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    msg = await message.answer('Неверный формат номера, введите номер в правильном формате')
    register_temporary_messages_repository.append(msg)


async def dont_enter_phone(call: types.CallbackQuery, ):
    msg = await call.message.answer('Окей, идентификация по tg id')
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    await asyncio.sleep(message_delete_delay)
    await bot.delete_message(msg.chat.id, msg.message_id)


async def service_is_not_alive_msg(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    msg = await message.answer('В текущий момент сервис отключен, пожалуйста, повторите позже')
    
    if state:
        print('state',state)
        await state.finish()

    await asyncio.sleep(message_delete_delay)
    await bot.delete_message(msg.chat.id, msg.message_id)


    messages_to_delete = register_temporary_messages_repository.read(chat_id)

    if messages_to_delete:
        for msg in messages_to_delete:
            await bot.delete_message(msg.chat.id, msg.message_id)
    
    register_temporary_messages_repository.delete(chat_id)


def check_is_service_alive():
    output = register_repository_sync.get_user(-228) 

    if output:
        if output.errors.timeout:
            return True
    return False


def register_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(
        ask_for_name_input,
        commands="start",
    )
    
    dp.register_message_handler(
        ask_for_phone_number_input,
        state=WaitForNameFSM.wait_for_name
    )

    dp.register_message_handler(service_is_not_alive_msg, lambda msg: check_is_service_alive(), state=WaitForContactFSM.wait_for_contact)

    dp.register_message_handler(
        wrong_phone_number_msg, lambda msg: phone_number_check_contact(msg), state=WaitForContactFSM.wait_for_contact, content_types="contact"
    )
    dp.register_message_handler(
        wrong_phone_number_msg, lambda msg: phone_number_check_text(msg), state=WaitForContactFSM.wait_for_contact
    )

    dp.register_message_handler(
        recieve_phone_number_contact, state=WaitForContactFSM.wait_for_contact, content_types="contact"
    )
    dp.register_message_handler(
        recieve_phone_number_text, state=WaitForContactFSM.wait_for_contact
    )
    dp.register_callback_query_handler(dont_enter_phone, text="dont_enter_phone")
    dp.register_callback_query_handler(enter_phone, text="enter_phone")
