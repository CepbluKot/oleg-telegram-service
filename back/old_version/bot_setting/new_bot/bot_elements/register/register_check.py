from aiogram import types, Dispatcher
from bot_elements.getters.register_getters import register_data_check_is_registered


async def checker(message: types.Message):
    await message.answer(' Вы не можете ничего делать, пока вы не зарегистрированы')
    

def register_handler_register_check(dp: Dispatcher):
    dp.register_message_handler(
        checker, lambda message: (not register_data_check_is_registered(message.chat.id)) and message.text.startswith('/'))
