from abc import ABC, abstractmethod

from bot_modules.settings.data_structures import Settings


class SettingsRepositoryInterface(ABC):
    @abstractmethod
    def get_user_settings(self, user_id: str) -> Settings:
        raise NotImplemented

    @abstractmethod
    def set_schedule_notifications_switch(self, user_id: str, state: bool):
        raise NotImplemented

    @abstractmethod
    def set_schedule_notifications_delay(self, user_id: str, delay: int):
        raise NotImplemented
