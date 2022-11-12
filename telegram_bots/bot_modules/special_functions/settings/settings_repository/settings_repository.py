from typing import Dict
from bot_modules.settings.data_structures import Settings
from bot_modules.special_functions.settings.settings_repository.settings_repository_interface import (
    SettingsRepositoryInterface,
)
from bot_modules.settings.settings_repository.settings_repository import (
    settings_repository,
)


class SettingRepository(SettingsRepositoryInterface):
    def get_user_settings(self, user_id: str) -> Settings:
        if str(user_id) in settings_repository.keys():
            return settings_repository[str(user_id)]

    def set_message_delete_switch(self, user_id: str, state: bool):
        settings_repository[str(user_id)].message_delete_switch = state

    def set_message_delete_delay(self, user_id: str, delay: int):
        settings_repository[str(user_id)].message_delete_delay = delay
