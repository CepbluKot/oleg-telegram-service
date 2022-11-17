# from telegram_bots.modules.register.repository.repository_abstraction import RegisterRepositoryAbstraction
from telegram_bots.modules.register.repository.repository_realisation import RegisterRepositoryRealisationDatabase
from telegram_bots.api.api import Api
from telegram_bots.modules.register.data_structures import User

import asyncio
register_repository_realisation_database = RegisterRepositoryRealisationDatabase()
# register_repository_abstraction = RegisterRepositoryAbstraction(register_repository_realisation_database)





async def main():
    us = User(name='vitalik', tg_id=-1000, phone='+7 999 123 88 88')
    print(await register_repository_realisation_database.add_user(us))

asyncio.run(main())
