import asyncio
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telegram_bots.modules.register.handlers import register_registration_handlers
from telegram_bots.bots import bot


async def main():
    bot_dispatcher = Dispatcher(
        bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )
 
    register_registration_handlers(bot_dispatcher)



    await asyncio.gather(
        bot_dispatcher.start_polling()
    )

asyncio.run(main())
