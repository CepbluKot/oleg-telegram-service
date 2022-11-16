from aiogram import Bot
import json, asyncio

with open("./config.json") as file:
    config = json.load(file)

loop = asyncio.get_event_loop()
bot = Bot(token=config["BOT_TOKEN"], loop=loop)
