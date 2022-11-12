from aiogram import Dispatcher, types
import bot_modules.cancel.cancel_handler


def create_cancel_handler(dp: Dispatcher):
    cancel_handler = bot_modules.cancel.cancel_handler.register_handlers_cancel(dp)
    return cancel_handler
