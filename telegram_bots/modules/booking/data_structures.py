from pydantic import BaseModel
from telegram_bots.modules.register.data_structures import User


class BookingMenu(BaseModel):
    page_id: int
    current_message_id: int


class Service(BaseModel):
    id: int
    name_service: str


class Booking(BaseModel):
    booking_day_end: str
    booking_day_start: str
    booking_time_end: str
    booking_time_start: str
    comment: str
    connect_event: int
    connect_user: User
    id_booking: int
    subscription_service: Service
