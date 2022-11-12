from bot_modules.special_functions.settings.settings_repository.settings_repository import (
    SettingRepository,
)
from bot_modules.special_functions.settings.settings_repository.settings_repository_abstraction import (
    SettingRepositoryAbstraction,
)


settings_repository = SettingRepository()
settings_repository_abs = SettingRepositoryAbstraction(settings_repository)
