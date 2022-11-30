from abc import abstractmethod, ABC
import typing
from telegram_bots.modules.booking.data_structures import Booking
from api.data_structures import ApiOutput


class BookingRepositoryInterface(ABC):
    @abstractmethod
    async def get_users_bookings(self, tg_id: int) -> ApiOutput:
        raise NotImplemented

    @abstractmethod
    async def delete_booking(self, booking_id: int) -> ApiOutput:
        raise NotImplemented
