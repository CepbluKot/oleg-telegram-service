import asyncio

from backend.storage import storage
from telegram_bots.bots import bot
from telegram_bot import launch_tg_bot

async def z():
    await launch_tg_bot()

asyncio.run(z())


