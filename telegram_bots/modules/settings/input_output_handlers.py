from aiogram import Dispatcher, types

from bot_modules.settings.settings_handlers.settings_handlers import SettingsHandlers
from bot_modules.settings.settings_handlers.settings_handlers_abstraction import (
    SettingsHandlersAbstraction,
)


def create_settings_handlers(dp: Dispatcher):
    settings_handlers = SettingsHandlers()
    settings_handlers_abs = SettingsHandlersAbstraction(settings_handlers)
    return settings_handlers_abs.settings_handlers_registrator(dp)
