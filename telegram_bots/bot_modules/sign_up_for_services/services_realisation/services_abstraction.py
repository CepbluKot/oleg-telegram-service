from bot_modules.sign_up_for_services.services_realisation.services_interface import (
    ServicesInterface,
)


class ServicesAbstraction(ServicesInterface):
    def __init__(self, interface: ServicesInterface) -> None:
        self.interface = interface

    def get_all_services(self):
        return self.interface.get_all_services()

    def get_service_data(self, service_id: str):
        return self.interface.get_service_data(service_id=service_id)

    def get_service_days(self, service_id: str):
        return self.interface.get_service_days(service_id=service_id)

    def get_service_weeks(self, service_id):
        return self.interface.get_service_weeks(service_id=service_id)

    def get_service_id_by_name(self, service_name):
        return self.interface.get_service_id_by_name(service_name=service_name)

    def send_chosen_service_data(
        self, service_id, service_week, service_day, user_id: str
    ):
        return self.interface.send_chosen_service_data(
            service_id=service_id,
            service_week=service_week,
            service_day=service_day,
            user_id=user_id,
        )
