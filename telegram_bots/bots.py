from aiogram import Bot
import json

with open("./telegram_bots/config.json") as file:
    config = json.load(file)

demo_bot = Bot(token=config["demoBotToken"])
admin_ids = config["adminIds"]
