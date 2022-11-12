from aiogram import Dispatcher, types

import bot_modules.register.register_handlers.register_handlers_abstraction
import bot_modules.register.register_handlers.register_handlers_realisation


def create_register_handlers(dp: Dispatcher):
    register = bot_modules.register.register_handlers.register_handlers_realisation.CustomersHandlers()
    register_abs = bot_modules.register.register_handlers.register_handlers_abstraction.CustomerHandlersAbstraction(register)
    return register_abs.register_handlers_registrator(dp)
