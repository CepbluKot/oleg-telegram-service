from typing import Dict
from bot_modules.settings.data_structures import Settings
from bot_modules.settings.settings_repository.settings_repository_interface import (
    SettingsRepositoryInterface,
)


settings_repository: Dict[str, Settings] = {}  # user_id: Settings


class SettingRepository(SettingsRepositoryInterface):
    def add_user(self, user_id: str):
        if str(user_id) not in settings_repository:
            settings_repository[str(user_id)] = Settings()

    def get_user_settings(self, user_id: str) -> Settings:
        if str(user_id) in settings_repository.keys():
            return settings_repository[str(user_id)]

    def set_message_delete_switch(self, user_id: str, state: bool):
        settings_repository[str(user_id)].message_delete_switch = state

    def set_message_delete_delay(self, user_id: str, delay: int):
        settings_repository[str(user_id)].message_delete_delay = delay

    def set_schedule_notifications_switch(self, user_id: str, state: bool):
        settings_repository[str(user_id)].schedule_notifications_switch = state

    def set_schedule_notifications_delay(self, user_id: str, delay: int):
        settings_repository[str(user_id)].schedule_notifications_delay = delay

    def set_forms_notification_switch(self, user_id: str, state: bool):
        settings_repository[str(user_id)].forms_notification_switch = state
