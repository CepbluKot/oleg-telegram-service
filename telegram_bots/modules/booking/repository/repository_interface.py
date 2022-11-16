from abc import abstractmethod, ABC
from typing import List



class BookingRepositoryInterface(ABC):
    @abstractmethod
    def get_users_bookings(self, tg_id: int):
        raise NotImplemented
