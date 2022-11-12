from aiogram import Dispatcher, types

import bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_abstraction
import bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_realisation

import bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_abstraction
import bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_realisation

import bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_abstraction
import bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_realisation

import bot_modules.forms.settings.settings_handlers.settings_handlers_abstraction
import bot_modules.forms.settings.settings_handlers.settings_handlers


def create_forms_handdlers(dp: Dispatcher):
    constructor = bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_realisation.FormsConstructorHandlersRealisation()
    constructor_abs = bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_abstraction.FormsConstructorHandlersAbstracation(constructor)
    
    editor = bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_realisation.FormsEditorHandlersRealisation()
    editor_abs = bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_abstraction.FormsEditorHandlersAbstraction(editor)
    
    menu = bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_realisation.FormsMenuHandlersRealisation()
    menu_abs = bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_abstraction.FormsMenuHandlersAbstraction(menu)
    
    settings = bot_modules.forms.settings.settings_handlers.settings_handlers.FormsSettingsHandlers()
    settings_abs = bot_modules.forms.settings.settings_handlers.settings_handlers_abstraction.FormsSettingsHandlersAbstraction(settings)

    constructor_abs.forms_constructor_habdlers_registrartor(dp)
    menu_abs.forms_menu_handlers_registrator(dp)
    editor_abs.forms_editor_handlers_registrator(dp)
    settings_abs.settings_handlers_registrator(dp)
