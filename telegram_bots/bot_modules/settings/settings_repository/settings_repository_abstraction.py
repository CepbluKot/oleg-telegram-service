from bot_modules.settings.data_structures import Settings
from bot_modules.settings.settings_repository.settings_repository_interface import (
    SettingRepositoryInterface,
)


class SettingRepositoryAbstraction(SettingRepositoryInterface):
    def __init__(self, interface: SettingRepositoryInterface) -> None:
        self.interface = interface

    def add_user(self, user_id: str):
        return self.interface.add_user(user_id=user_id)

    def get_user_settings(self, user_id: str) -> Settings:
        return self.interface.get_user_settings(user_id=user_id)

    def set_message_delete_switch(self, user_id: str, state: bool):
        return self.interface.set_message_delete_switch(user_id=user_id, state=state)

    def set_message_delete_delay(self, user_id: str, delay: int):
        return self.interface.set_message_delete_delay(user_id=user_id, delay=delay)

    def set_schedule_notifications_switch(self, user_id: str, state: bool):
        return self.interface.set_schedule_notifications_switch(
            user_id=user_id, state=state
        )

    def set_schedule_notifications_delay(self, user_id: str, delay: int):
        return self.interface.set_schedule_notifications_delay(
            user_id=user_id, delay=delay
        )

    def set_forms_notification_switch(self, user_id: str, state: bool):
        return self.interface.set_forms_notification_switch(
            user_id=user_id, state=state
        )
