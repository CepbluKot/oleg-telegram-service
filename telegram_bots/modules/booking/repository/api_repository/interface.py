from abc import abstractmethod, ABC
import typing
from telegram_bots.modules.booking.data_structures import Booking


class BookingRepositoryInterface(ABC):
    @abstractmethod
    async def get_users_bookings(self, tg_id: int) -> typing.List[Booking]:
        raise NotImplemented
