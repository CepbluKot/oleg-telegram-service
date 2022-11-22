from threading import current_thread
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from telegram_bots.modules.register.handlers import register_registration_handlers
from telegram_bots.bots import bot
from telegram_bots.modules.booking.handlers import register_booking_handlers
from backend.storage import storage


async def __launch_notifications_daemon():
    while current_thread().isAlive():
        await asyncio.sleep(0.001)
        while storage:
            notification = storage.pop()
            await bot.send_message(notification.tg_id, notification.text)


async def __commands(bot: Bot):
    commands = [
        BotCommand(command="/my_bookings", description="Мои записи"),
    ]
    await bot.set_my_commands(commands)


async def launch_tg_bot():
    bot_dispatcher = Dispatcher(
        bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )
    bot_dispatcher.loop.create_task(__launch_notifications_daemon())
    bot_dispatcher.loop.create_task(__commands(bot))
    
    register_registration_handlers(bot_dispatcher)
    register_booking_handlers(bot_dispatcher)

    await asyncio.gather(
        bot_dispatcher.start_polling()
    )
