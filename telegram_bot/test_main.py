import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_modules.cancel.cancel_handler import register_handlers_cancel
from bot_modules.settings.settings_handlers.settings_handlers import SettingsHandlers
from bot_modules.settings.settings_handlers.settings_handlers_abstraction import (
    SettingsHandlersAbstraction,
)


from bots import student_bot, prepod_bot, admin_bot, customer_bot

from bot_modules.register.register_handlers.register_handlers_abstraction import (
    PrepodHandlersAbstraction,
    StudentHandlersAbstraction,
    CustomerHandlersAbstraction
)
from bot_modules.register.register_handlers.register_handlers_realisation import (
    PrepodHandlers,
    StudentHandlers,
    CustomersHandlers
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



async def customer_commands(bot: Bot):
    student_commands = [
        BotCommand(command="/register", description="Регистация"),
        # BotCommand(command="/status", description="Полученные формы"),
        # BotCommand(command="/settings", description="Настройки"),
        # BotCommand(command="/cancel", description="Отменить текущее действие"),
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

    customer_bot_dispatcher = Dispatcher(
        customer_bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )

    prepod_bot_dispatcher.loop.create_task(prepod_commands(prepod_bot))
    student_bot_dispatcher.loop.create_task(student_commands(student_bot))
    admin_bot_dispatcher.loop.create_task(admin_commands(admin_bot))
    customer_bot_dispatcher.loop.create_task(customer_commands(customer_bot))

    customer_reg = CustomersHandlers()
    customer_reg_abs = CustomerHandlersAbstraction(customer_reg)

    customer_reg_abs.register_handlers_registrator(dp=customer_bot_dispatcher)

    await asyncio.gather(
        # prepod_bot_dispatcher.start_polling(),
        # student_bot_dispatcher.start_polling(),
        # admin_bot_dispatcher.start_polling(),
        customer_bot_dispatcher.start_polling()
    )

asyncio.run(main())
