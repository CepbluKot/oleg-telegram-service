import typing
from telegram_bots.modules.booking.repository.api_repository.interface import (
    BookingRepositoryInterface
)
from telegram_bots.modules.booking.data_structures import Booking
from api.data_structures import ApiOutput


class BookingRepositoryAbstractionAsync(BookingRepositoryInterface):
    def __init__(self, interface: BookingRepositoryInterface) -> None:
        self.interface = interface

    async def get_users_bookings(self, tg_id: int) -> ApiOutput:
        return await self.interface.get_users_bookings(tg_id=tg_id)

    async def delete_booking(self,  booking_id: int) -> ApiOutput:
        return await self.interface.delete_booking( booking_id=booking_id)
