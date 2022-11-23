from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from telegram_bots.modules.register.repository.api_repository.output import register_repository_abstraction


class RegistrationFSM(StatesGroup):
    waif_for_contact = State()


async def ask_for_phone_number_input(message: types.Message):
    response = await register_repository_abstraction.get_user(message.from_user.id)
    
    if response and not response.is_exception:
        if response.tg_id == message.chat.id:
            await message.answer("Вы уже зарегистрированы")

        else:
            buttons = [
                    types.InlineKeyboardButton(
                        text="Да", callback_data="enter_phone"),
                    types.InlineKeyboardButton(
                        text="Нет", callback_data="dont_enter_phone"),
                ]
            
            await message.answer("Хотите ввести свой номер телефона?", reply_markup=buttons)
    
    else:
        message.answer("В настоящий момент сервис не доступен, пожалуйста. повторите позже")


async def ask_phone_number(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    send_phone_number_button = types.KeyboardButton(
        text="Отправить номер телефона", request_contact=True
    )
    keyboard.add(send_phone_number_button)
    await message.answer(
        "Отправьтей свой контакт или введите номер телефона вручную", reply_markup=keyboard
    )
    await RegistrationFSM.waif_for_contact.set()


async def recieve_phone_number_contact(message: types.Message, state: FSMContext):
    await message.answer("Регистрация завершена", reply_markup=None)
    print('contct',  message.contact)
    # print('message.contact.phone_number', message.contact.phone_number, 'text', message.text)
    # do smth in api
    await state.finish()


async def recieve_phone_number_text(message: types.Message, state: FSMContext):
    await message.answer("Регистрация завершена", reply_markup=None)
    print('text', message.text)
    # print('message.contact.phone_number', message.contact.phone_number, 'text', message.text)
    # do smth in api
    await state.finish()


async def wrong_phone_number():
    pass
    # неверный формат номера, повторите ввод


async def dont_enter_phone(call: types.callback_query):
    await call.Message.answer('Окей, идентификация по tg id')


def register_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(
        ask_for_phone_number_input,
        commands="start",
    )
    dp.register_message_handler(
        recieve_phone_number_contact, state=RegistrationFSM.waif_for_contact, content_types="contact"
    )
    dp.register_message_handler(
        recieve_phone_number_text, state=RegistrationFSM.waif_for_contact
    )
    dp.register_callback_query_handler(dont_enter_phone, text="dont_enter_phone")
    dp.register_callback_query_handler(ask_phone_number, text="enter_phone")
