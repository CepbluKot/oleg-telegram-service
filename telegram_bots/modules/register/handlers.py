from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from telegram_bots.modules.register.repository.output import register_repository_abstraction


class WaitForContactFSM(StatesGroup):
    waif_for_contact = State()


async def ask_phone_number(message: types.Message, state: FSMContext):
    response = await register_repository_abstraction.get_user(message.from_user.id)
    
    if not response.is_exception:
        if response.data.tg_id == message.chat.id:
            await message.answer("Вы уже зарегистрированы")

    else:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        send_phone_number_button = types.KeyboardButton(
            text="Отправить номер телефона", request_contact=True
        )
        keyboard.add(send_phone_number_button)
        await message.answer(
            "Для работы уведомлений требуется ваш номер телефона", reply_markup=keyboard
        )
        await WaitForContactFSM.waif_for_contact.set()


async def final(message: types.Message, state: FSMContext):
    await message.answer("Регистрация завершена", reply_markup=None)
    print(message.contact.phone_number)
    # do smth in api
    await state.finish()




async def already_registered_check(message: types.Message):
    return await register_repository_abstraction.get_user(message.from_user.id)


def register_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(
        ask_phone_number,
        commands="start",
    )
    dp.register_message_handler(
        final, state=WaitForContactFSM.waif_for_contact, content_types="contact"
    )
