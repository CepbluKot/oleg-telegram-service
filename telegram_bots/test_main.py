import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bots import demo_bot

import bot_modules.register.input_output_handlers
import bot_modules.sign_up_for_services.input_output_handlers
import bot_modules.forms.input_output_handlers
import bot_modules.settings.input_output_handlers
import bot_modules.cancel.input_output_handlers
import bot_modules.user_interface.input_output_handlers
import bot_modules.special_functions.input_output_handlers
import bot_modules.sign_up_for_services.input_output_handlers

async def demo_commands(bot: Bot):
    commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/sign_up_for_service", description="Записаться на услугу"),
        BotCommand(command="/multi_form", description="Создать форму для опроса"),
        BotCommand(command="/saved_forms", description="Посмотреть сохраненные опросы"),
        BotCommand(command="/status_for_creator", description="Отобразить отправленные опросы"),
        BotCommand(command="/status_for_user", description="Отобразить полученные опросы"),
        BotCommand(command="/settings", description="Настройки"),
        BotCommand(command="/cancel", description="Отменить текущее действие"),
    ]

    await bot.set_my_commands(commands)


async def main():
    demo_bot_dispatcher = Dispatcher(
        demo_bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )
 
    demo_bot_dispatcher.loop.create_task(demo_commands(demo_bot))

    bot_modules.register.input_output_handlers.create_register_handlers(demo_bot_dispatcher)
    bot_modules.sign_up_for_services.input_output_handlers.create_sign_up_handlers(demo_bot_dispatcher)
    bot_modules.user_interface.input_output_handlers.create_form_creator_ui_handlers(demo_bot_dispatcher)
    bot_modules.user_interface.input_output_handlers.create_client_ui_handlers(demo_bot_dispatcher)
    bot_modules.forms.input_output_handlers.create_forms_handdlers(demo_bot_dispatcher)

    bot_modules.settings.input_output_handlers.create_settings_handlers(demo_bot_dispatcher)
    bot_modules.special_functions.input_output_handlers.create_special_functions_handlers(demo_bot_dispatcher)
    bot_modules.sign_up_for_services.input_output_handlers.create_sign_up_handlers(demo_bot_dispatcher)
    bot_modules.cancel.input_output_handlers.create_cancel_handler(demo_bot_dispatcher)


    await asyncio.gather(
        demo_bot_dispatcher.start_polling()
    )

asyncio.run(main())
