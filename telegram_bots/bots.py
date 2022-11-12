from aiogram import Bot
import json, asyncio

with open("./telegram_bots/config.json") as file:
    config = json.load(file)

loop = asyncio.get_event_loop()


demo_bot = Bot(token=config["demoBotToken"], loop=loop)
admin_ids = config["adminIds"]
