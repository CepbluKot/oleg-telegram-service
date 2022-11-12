from abc import ABC, abstractmethod


class ServicesInterface(ABC):
    @abstractmethod
    def get_all_services(self):
        raise NotImplemented

    @abstractmethod
    def get_service_data(self, service_id: str):
        raise NotImplemented

    @abstractmethod
    def get_service_days(self, service_id: str):
        raise NotImplemented

    @abstractmethod
    def get_service_weeks(self, service_id):
        raise NotImplemented

    @abstractmethod
    def get_service_id_by_name(self, service_name):
        raise NotImplemented

    @abstractmethod
    def send_chosen_service_data(
        self, service_id, service_week, service_day, user_id: str
    ):
        raise NotImplemented
