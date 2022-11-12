from bot_modules.schedule.settings.settings_repository.settings_repository_interface import (
    SettingsRepositoryInterface,
)
from bot_modules.settings.data_structures import Settings


class SettingRepositoryAbstraction(SettingsRepositoryInterface):
    def __init__(self, interface: SettingsRepositoryInterface) -> None:
        self.interface = interface

    def get_user_settings(self, user_id: str) -> Settings:
        return self.interface.get_user_settings(user_id=user_id)

    def set_schedule_notifications_switch(self, user_id: str, state: bool):
        return self.interface.set_schedule_notifications_switch(
            user_id=user_id, state=state
        )

    def set_schedule_notifications_delay(self, user_id: str, delay: int):
        return self.interface.set_schedule_notifications_delay(
            user_id=user_id, delay=delay
        )
