from typing import List
from bot_modules.sign_up_for_services.services_realisation.services_interface import (
    ServicesInterface,
)
from pydantic import BaseModel
# import adapter_tg.adapter_tg

class Service(BaseModel):
    service_id: str
    service_name: str
    service_weeks: List[str]
    service_days: List[str]


services = {
    "1": Service(
        service_id=0,
        service_name="Услуга 1",
        service_weeks=["01.01.2022 - 08.01.2022", "08.01.2022 - 15.01.2022"],
        service_days=["1", "2", "3"],
    ),
    "2": Service(
        service_id=1,
        service_name="Услуга 2",
        service_weeks=["15.01.2022 - 22.01.2022"],
        service_days=["1", "2", "3"],
    ),
    "3": Service(
        service_id=2,
        service_name="Услуга 3",
        service_weeks=[
            "02.02.2022 - 09.02.2022",
            "10.02.2022 - 17.02.2022",
            "18.02.2022 - 25.02.2022",
        ],
        service_days=["1", "2", "3"],
    ),
}


class Services(ServicesInterface):
    def get_all_services(self):
        return services

    def get_service_data(self, service_id: str) -> Service:
        return services[str(service_id)]

    def get_service_days(self, service_id: str):
        
        return services[str(service_id)].service_days

    def get_service_weeks(self, service_id):
        return services[str(service_id)].service_weeks


    def get_service_id_by_name(self, service_name):
        for service_id in services:
            if services[service_id].service_name == service_name:
                return service_id

    def send_chosen_service_data(
        self, service_id, service_week, service_day, user_id: str
    ):
        print("service information sent: ", service_id, service_day, service_week)
