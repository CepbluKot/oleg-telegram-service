import asyncio

from telegram_bots.modules.register.data_structures import User
from telegram_bots.modules.booking.repository.api_repository.output import booking_repository_abstraction
from telegram_bots.modules.register.repository.api_repository.output import register_repository_async, register_repository_sync


async def main():
    usr = User(name='olega', tg_id=2, phone='89005354444')
    await booking_repository_abstraction.get_users_bookings(23)

asyncio.run(main())
