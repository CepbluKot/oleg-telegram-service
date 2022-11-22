# from telegram_bots.modules.register.repository.repository_abstraction import RegisterRepositoryAbstraction
from telegram_bots.modules.register.repository.repository_realisation import (
    RegisterRepositoryRealisationDatabase,
)
from telegram_bots.modules.booking.repository.api_repository.output import (
    booking_repository_abstraction
)

from telegram_bots.api.api import Api
from telegram_bots.modules.register.data_structures import User

import asyncio

# from telegram_bots.modules.register.backend.realisation import RegisterBackend
from telegram_bots.modules.register.repository.output import register_repository_abstraction


async def main():
    user = User(name="vitalik", tg_id=123, phone="+79151311726")
    # x = RegisterBackend()
    # resp = await x.update_users_registration(
    #     phone_number="88005553535", telegram_id=123
    # )

    # resp = await register_repository_abstraction.get_user(4)
    resp = await booking_repository_abstraction.get_users_bookings(3)

    if not resp:
        print("not available")

    else:
        print(resp)


asyncio.run(main())
