import json, datetime, time
from typing import List
from telegram_bots.modules.booking.data_structures import User, Booking, Service
from telegram_bots.modules.booking.repository.api_repository.interface import (
    BookingRepositoryInterface,
)
from aiohttp.client_reqrep import ClientResponse
from requests import Response


from api.api import ApiAsync
from api.data_structures import ApiOutput, ErrorType
from api.error_handler.error_handler import handle_error_async_api

# from faker import Faker
# fake = Faker(locale='ru_RU')


# usr = User(name='olega', tg_id=14, phone='89005553535')
# services = [Service(id=n, name_service=fake.job()) for n in range(12)]
# sample = [Booking(booking_day_start=str(datetime.date.today()), booking_time_start=str(time.ctime()), booking_day_end=str(datetime.date.today()), booking_time_end=str(time.ctime()), comment=f' booka {x}', connect_event=0, connect_user=usr, subscription_service=services[x], id_booking=0) for x in range(12)]



class BookingRepositoryRealisationDatabase(BookingRepositoryInterface):
    def __init__(self) -> None:
        __connection_data = self.__get_connection_data()
        self.url = __connection_data["BOOKING_URL"]

    def __get_connection_data(self):
        with open("config.json", "r") as f:
            connection_data = json.loads(f.read())
        return connection_data

    async def __error_checker(self, response: ClientResponse):
        response_text = await response.text()

        if response:
            return handle_error_async_api(response=response, response_text=response_text)

        elif not response:
            return ErrorType(timeout=True, has_error=True)

    async def get_users_bookings(self, tg_id: int) -> ApiOutput:
        api = ApiAsync()
        bookings = []
        output, response_text = await api.get(
            url_path=self.url + "/my_booking", params={"id_tg": tg_id}
        )
        error_check = await self.__error_checker(response)

        if not error_check.has_error:
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
        

        output = ApiOutput(errors=error_check, data=bookings)
        return output


    async def delete_booking(self,  booking_id: int) -> ApiOutput:
        api = ApiAsync()
        output, response_text = await api.delete(
            url_path=self.url, params={"id_bookings": booking_id}
        )

        error_check = await self.__error_checker(response)

        
        if not error_check.has_error:
            return ApiOutput(data=True, errors=error_check)

        return ApiOutput(data=False, errors=error_check)
