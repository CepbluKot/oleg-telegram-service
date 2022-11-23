import typing
from telegram_bots.modules.booking.repository.api_repository.interface import (
    BookingRepositoryInterface
)
from telegram_bots.modules.booking.data_structures import Booking


class BookingRepositoryAbstraction(BookingRepositoryInterface):
    def __init__(self, interface: BookingRepositoryInterface) -> None:
        self.interface = interface

    def get_users_bookings(self, tg_id: int) -> typing.List[Booking]:
        return self.interface.get_users_bookings(tg_id=tg_id)

    def delete_booking(self, client_id: int, booking_id: int) -> typing.List[Booking]:
        return self.interface.delete_booking(client_id=client_id, booking_id=booking_id)
