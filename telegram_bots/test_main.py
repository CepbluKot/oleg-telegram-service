import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_modules.cancel.cancel_handler import register_handlers_cancel
from bot_modules.settings.settings_handlers.settings_handlers import SettingsHandlers
from bot_modules.settings.settings_handlers.settings_handlers_abstraction import (
    SettingsHandlersAbstraction,
)


from bots import student_bot, prepod_bot, admin_bot

from bot_modules.register.register_handlers.register_handlers_abstraction import (
    PrepodHandlersAbstraction,
    StudentHandlersAbstraction,
)
from bot_modules.register.register_handlers.register_handlers_realisation import (
    PrepodHandlers,
    StudentHandlers,
)

from bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_realisation import (
    FormsConstructorHandlersRealisation,
)
from bot_modules.forms.forms_handlers.forms_constructor.forms_constructor_handlers_abstraction import (
    FormsConstructorHandlersAbstracation,
)

from bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_abstraction import (
    FormsEditorHandlersAbstraction,
)
from bot_modules.forms.forms_handlers.forms_editor.forms_editor_handlers_realisation import (
    FormsEditorHandlersRealisation,
)

from bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_realisation import (
    FormsMenuHandlersRealisation,
)
from bot_modules.forms.forms_handlers.forms_menu.forms_menu_handlers_abstraction import (
    FormsMenuHandlersAbstraction,
)
from bot_modules.user_interface.ui_handlers.ui_handlers import (
    PrepodHandlersStatus,
    StudentHandlersStatus,
)
from bot_modules.user_interface.ui_handlers.ui_handlers_abstraction import (
    PrepodHandlersStatusAbstraction,
    StudentHandlersStatusAbstraction,
)

from bot_modules.useless_messages_handler import useless_message_handler_registerer


async def prepod_commands(bot: Bot):
    prepod_commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/multi_form", description="Создать форму"),
        BotCommand(command="/saved_forms", description="Посмотреть сохраненные формы"),
        BotCommand(command="/status", description="Отобразить статус"),
        BotCommand(command="/settings", description="Настройки"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
    ]

    await bot.set_my_commands(prepod_commands)


async def student_commands(bot: Bot):
    student_commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/status", description="Полученные формы"),
        BotCommand(command="/settings", description="Настройки"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
    ]
    await bot.set_my_commands(student_commands)


async def admin_commands(bot: Bot):
    student_commands = [
        BotCommand(
            command="/check_current_creating_forms",
            description="Создаваемые сейчас формы",
        ),
        BotCommand(command="/check_created_forms", description="Все созданные формы"),
        BotCommand(command="/check_sent_forms", description="Отправленные формы"),
        BotCommand(command="/check_completing_forms", description="Выполняемые формы"),
        BotCommand(
            command="/check_unregistered_users",
            description="Пользователи, ожидающие подтверждения регистрации",
        ),
        BotCommand(
            command="/check_edited_users",
            description="Пользователи, ожидающие подтверждения изменения данных",
        ),
        BotCommand(
            command="/get_student_list",
            description="Получить список студентов по группе (напишите номер группы)",
        ),
    ]
    await bot.set_my_commands(student_commands)


async def main():
    prepod_bot_dispatcher = Dispatcher(
        prepod_bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )

    student_bot_dispatcher = Dispatcher(
        student_bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )

    admin_bot_dispatcher = Dispatcher(
        admin_bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )

    prepod_bot_dispatcher.loop.create_task(prepod_commands(prepod_bot))
    student_bot_dispatcher.loop.create_task(student_commands(student_bot))
    admin_bot_dispatcher.loop.create_task(admin_commands(admin_bot))

    prepod_reg = PrepodHandlers()
    stud_reg = StudentHandlers()

    prep_reg_abs = PrepodHandlersAbstraction(prepod_reg)
    stud_reg_abs = StudentHandlersAbstraction(stud_reg)

    constructor = FormsConstructorHandlersRealisation()
    constructor_abs = FormsConstructorHandlersAbstracation(constructor)

    edit = FormsEditorHandlersRealisation()
    edit_abs = FormsEditorHandlersAbstraction(edit)

    menu = FormsMenuHandlersRealisation()
    menu_abs = FormsMenuHandlersAbstraction(menu)

    prepod_status = PrepodHandlersStatus()
    prepod_status_abs = PrepodHandlersStatusAbstraction(prepod_status)

    student_status = StudentHandlersStatus()
    student_status_abs = StudentHandlersStatusAbstraction(student_status)

    settings = SettingsHandlers()
    settings_abs = SettingsHandlersAbstraction(settings)

    prepod_status_abs.register_handlers_prepod_status(prepod_bot_dispatcher)
    student_status_abs.register_handlers_student_status(student_bot_dispatcher)

    prep_reg_abs.prepod_registration_handlers_registrator(prepod_bot_dispatcher)
    stud_reg_abs.student_registration_handlers_register(student_bot_dispatcher)
    edit_abs.forms_editor_handlers_registrator(prepod_bot_dispatcher)
    constructor_abs.forms_constructor_habdlers_registrartor(prepod_bot_dispatcher)
    menu_abs.forms_menu_handlers_registrator(prepod_bot_dispatcher)
    settings_abs.settings_handlers_registrator(student_bot_dispatcher)
    settings_abs.settings_handlers_registrator(prepod_bot_dispatcher)

    register_handlers_cancel(student_bot_dispatcher)
    register_handlers_cancel(prepod_bot_dispatcher)

    useless_message_handler_registerer(student_bot_dispatcher)

    await asyncio.gather(
        prepod_bot_dispatcher.start_polling(),
        student_bot_dispatcher.start_polling(),
        admin_bot_dispatcher.start_polling(),
    )


asyncio.run(main())
