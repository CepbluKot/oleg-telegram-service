# from telegram_bots.modules.register.repository.repository_abstraction import RegisterRepositoryAbstraction
from telegram_bots.modules.register.repository.repository_realisation import RegisterRepositoryRealisationDatabase

import asyncio
register_repository_realisation_database = RegisterRepositoryRealisationDatabase()
# register_repository_abstraction = RegisterRepositoryAbstraction(register_repository_realisation_database)


async def main():
    loop = asyncio.get_event_loop()
    print(await register_repository_realisation_database.get_user(1111, loop=loop))


asyncio.run(main())
