from telegram_bots.modules.booking.repository.repository_interface import BookingRepositoryInterface


class BookingRepositoryAbstraction(BookingRepositoryInterface):
    def __init__(self, interface: BookingRepositoryInterface) -> None:
        self.interface = interface

    def get_users_bookings(self, tg_id: int):
        return self.interface.get_users_bookings(tg_id=tg_id)
