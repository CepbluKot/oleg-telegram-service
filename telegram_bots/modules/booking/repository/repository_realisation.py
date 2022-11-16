import json
from typing import List
from telegram_bots.modules.booking.data_structures import User, Booking, Service
from telegram_bots.modules.booking.repository.repository_interface import BookingRepositoryInterface
from telegram_bots.api.api import Api


class BookingRepositoryRealisationDatabase(BookingRepositoryInterface):
    def __init__(self) -> None:
        __connection_data = self.__get_connection_data()
        self.url = __connection_data["BOOKING_URL"]
        self.api = Api()
    
    def __get_connection_data(self):
        with open('config.json', 'r') as f:
            connection_data = json.loads(f.read())
        return connection_data

    async def get_users_bookings(self, tg_id: int) -> List[Booking]:
        bookings = []
        response = await self.api.get(url_path=self.url+'/my_booking', params={'id_client': tg_id})
        
        if not 'message' in response:
            for selected_booking in response:
                booking_day_end = selected_booking['booking_day_end']
                booking_day_start = selected_booking['booking_day_start']
                booking_time_end = selected_booking['booking_time_end']
                booking_time_start = selected_booking['booking_time_start']
                comment = selected_booking['comment']
                connect_event = selected_booking['connect_event']
                connect_user = User(name=selected_booking['connect_user']['name_client'], tg_id=selected_booking['connect_user']['tg_id'], phone=selected_booking['connect_user']['phone_num'])
                id_booking = selected_booking['id_booking']
                subscription_service = Service(id=selected_booking['subscription_service']['id'], name_service=selected_booking['subscription_service']['name_service'])

                parsed = Booking(booking_day_end=booking_day_end, booking_day_start=booking_day_start, booking_time_end=booking_time_end, 
                booking_time_start=booking_time_start, comment=comment, connect_event=connect_event, connect_user=connect_user,
                id_booking=id_booking, subscription_service=subscription_service)

                bookings.append(parsed)
    
        return bookings
