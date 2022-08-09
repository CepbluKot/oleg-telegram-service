import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_elements.cancel import register_handlers_cancel

from bot_elements.register.register_check import register_handler_register_check
from bot_elements.register.user_register import register_handler_register_user
from bot_elements.services.sign_up_for_services import register_handler_services
from bots import user_bot


async def user_commands(bot: Bot):
    commands = [
        BotCommand(command="/register", description="Регистация"),
        BotCommand(command="/select_service", description="Выбрать услугу"),
        BotCommand(command="/cancel", description="Отменить действие"),
    ]
    await bot.set_my_commands(commands)


async def main():
        
    user_bot_dispatcher = Dispatcher(user_bot, storage=MemoryStorage(),
                    loop=asyncio.get_event_loop())

    user_bot_dispatcher.loop.create_task(user_commands(user_bot))
    
    register_handlers_cancel(user_bot_dispatcher)
    
    register_handler_register_user(user_bot_dispatcher)
    register_handler_register_check(user_bot_dispatcher)
    
    register_handler_services(user_bot_dispatcher)
    await asyncio.gather(user_bot_dispatcher.start_polling())
    

asyncio.run(main())
