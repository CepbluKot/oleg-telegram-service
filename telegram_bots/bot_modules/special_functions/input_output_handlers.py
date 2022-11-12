from aiogram import Dispatcher, types

from bot_modules.special_functions.settings.settings_handlers.settings_handlers import SettingsHandlers
from bot_modules.special_functions.settings.settings_handlers.settings_handlers_abstraction import SettingsHandlersAbstraction


def create_special_functions_handlers(dp: Dispatcher):
    settings_handlers = SettingsHandlers()
    settings_handlers_abs = SettingsHandlersAbstraction(settings_handlers)
    return settings_handlers_abs.settings_handlers_registrator(dp)
