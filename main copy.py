import asyncio
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from telegram_bots.modules.register.handlers import register_registration_handlers
from telegram_bots.bots import bot
from telegram_bots.modules.booking.handlers import register_booking_handlers


async def commands(bot: Bot):
    commands = [
        BotCommand(command="/my_bookings", description="Мои записи"),
    ]
    await bot.set_my_commands(commands)


async def main():
    bot_dispatcher = Dispatcher(
        bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )
    bot_dispatcher.loop.create_task(commands(bot))
    register_registration_handlers(bot_dispatcher)
    register_booking_handlers(bot_dispatcher)
    await asyncio.gather(
        bot_dispatcher.start_polling()
    )

asyncio.run(main())
