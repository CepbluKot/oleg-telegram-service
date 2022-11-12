from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext


class WaitForContactFSM(StatesGroup):
    waif_for_contact = State()
    

async def ask_register_fio(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить телефон",
                                        request_contact=True)
    keyboard.add(button_phone)
    await message.answer( 'для дальнейшей работы требуется ваш номер телефона',
                        reply_markup=keyboard)

    await WaitForContactFSM.waif_for_contact.set()


async def final(message: types.Message, state: FSMContext):
    await message.answer('done',reply_markup='')
    print(message.contact.phone_number)
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(ask_register_fio, commands="contact", )
    dp.register_message_handler(final, state=WaitForContactFSM.waif_for_contact, content_types='contact')
