import asyncio, threading
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bots import demo_bot

import bot_modules.settings.input_output_handlers
import bot_modules.cancel.input_output_handlers

import bot_modules.test.get_contact 

import bot_backend.app
import bot_backend.storag


async def demo_commands(bot: Bot):
    commands = [
        BotCommand(command="/contact", description="тест контактов"),
        
    ]

    await bot.set_my_commands(commands)


async def periodic():
    while True:
        await asyncio.sleep(0.01)

        while bot_backend.storag.stor:
            a = bot_backend.storag.stor.pop()
            await demo_bot.send_message(text=a.text, chat_id=a.userid)

async def main():
    demo_bot_dispatcher = Dispatcher(
        demo_bot, storage=MemoryStorage(), loop=asyncio.get_event_loop()
    )
 
    demo_bot_dispatcher.loop.create_task(demo_commands(demo_bot))
    bot_modules.test.get_contact.register_handlers(demo_bot_dispatcher)
    bot_modules.cancel.input_output_handlers.create_cancel_handler(demo_bot_dispatcher)


    demo_bot_dispatcher.loop.create_task(periodic())

    await asyncio.gather(
        
        demo_bot_dispatcher.start_polling()
    )

thr1 = threading.Thread(target=bot_backend.app.app.run,)
thr2 = threading.Thread(target=asyncio.run, args=(main(), ))

thr2.start()
thr1.start()
