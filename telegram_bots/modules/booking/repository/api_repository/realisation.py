import json, datetime, time
from typing import List
from telegram_bots.modules.booking.data_structures import User, Booking, Service
from telegram_bots.modules.booking.repository.api_repository.interface import (
    BookingRepositoryInterface,
)
from api.api import ApiAsync


usr = User(name='olega', tg_id=14, phone='89005553535')
srv_0 = Service(id=0, name_service='Доставка бананов')
srv_1 = Service(id=1, name_service='Барбишоп')
srv_2 = Service(id=2, name_service='Раздача алмазов')

book_1 = Booking(booking_day_start=str(datetime.date.today()), booking_time_start=str(time.ctime()), booking_day_end=str(datetime.date.today()), booking_time_end=str(time.ctime()), comment='sampe comment booka 1', connect_event=0, connect_user=usr, subscription_service=srv_0, id_booking=0)
book_2 = Booking(booking_day_start=str(datetime.date.today()), booking_time_start=str(time.ctime()), booking_day_end=str(datetime.date.today()), booking_time_end=str(time.ctime()), comment='sampe comment booka 2', connect_event=0, connect_user=usr, subscription_service=srv_1, id_booking=1)
book_3 = Booking(booking_day_start=str(datetime.date.today()), booking_time_start=str(time.ctime()), booking_day_end=str(datetime.date.today()), booking_time_end=str(time.ctime()), comment='sampe comment booka 3', connect_event=0, connect_user=usr, subscription_service=srv_2, id_booking=2)

sample = [book_1, book_2, book_3]


class BookingRepositoryRealisationDatabase(BookingRepositoryInterface):
    def __init__(self) -> None:
        __connection_data = self.__get_connection_data()
        self.url = __connection_data["BOOKING_URL"]

    def __get_connection_data(self):
        with open("config.json", "r") as f:
            connection_data = json.loads(f.read())
        return connection_data

    def __is_exception(self, response: str):
        if response:
            if "available" in response or "message" in response:
                return True

        elif not response:
            return True
        
    async def get_users_bookings(self, tg_id: int) -> List[Booking]:
        api = ApiAsync()
        bookings = []
        response = await api.get(
            url_path=self.url + "/my_booking", params={"id_tg": tg_id}
        )
        
        if not self.__is_exception(response):
            response = json.loads(response)

            for selected_booking in response:

                booking_day_end = selected_booking["booking_day_end"]
                booking_day_start = selected_booking["booking_day_start"]
                booking_time_end = selected_booking["booking_time_end"]
                booking_time_start = selected_booking["booking_time_start"]
                comment = selected_booking["comment"]
                connect_event = selected_booking["connect_event"]
                connect_user = User(
                    name=selected_booking["connect_user"]["name_client"],
                    tg_id=selected_booking["connect_user"]["tg_id"],
                    phone=selected_booking["connect_user"]["phone_num"],
                )
                id_booking = selected_booking["id_booking"]

                if selected_booking["subscription_service"]:
                    
                    subscription_service = Service(
                        id=selected_booking["subscription_service"]["id"],
                        name_service=selected_booking["subscription_service"][
                            "name_service"
                        ])
                else:
                    subscription_service = Service()
                
                
                parsed = Booking(
                    booking_day_end=booking_day_end,
                    booking_day_start=booking_day_start,
                    booking_time_end=booking_time_end,
                    booking_time_start=booking_time_start,
                    comment=str(comment),
                    connect_event=connect_event,
                    connect_user=connect_user,
                    id_booking=id_booking,
                    subscription_service=subscription_service,
                )

                bookings.append(parsed)
        
        return bookings


    async def delete_booking(self, client_id: int, booking_id: int) -> List[Booking]:
        api = ApiAsync()
        response = await api.delete(
            url_path=self.url, params={"id_client": client_id, "id_bookings": booking_id}
        )
        if not self.__is_exception(response):
            return True
