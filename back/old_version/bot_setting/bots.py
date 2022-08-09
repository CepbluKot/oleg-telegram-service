from aiogram import Bot
import json


with open('config_bot.json') as file:
    config = json.load(file)


user_bot = Bot(token=config['userBotToken'])
