from aiogram import Dispatcher, types

from bot_modules.sign_up_for_services.services_handlers.services_handlers_abstraction import ChooseServiceHandlersAbstraction
from bot_modules.sign_up_for_services.services_handlers.services_handlers_realisation import ChooseServiceHandlers


def create_sign_up_handlers(dp: Dispatcher):
    choose_services = ChooseServiceHandlers()
    choose_services_abs = ChooseServiceHandlersAbstraction(choose_services)
    return choose_services_abs.services_handlers_registrator(dp)
