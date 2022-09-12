from aiogram import types, Dispatcher


async def useless_message_handler(message: types.Message):
    await message.delete()


def useless_message_handler_registerer(dp: Dispatcher):
    dp.register_message_handler(useless_message_handler)
