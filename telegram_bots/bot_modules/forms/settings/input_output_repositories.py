from bot_modules.forms.settings.settings_repository.settings_repository import (
    SettingsRepository,
)
from bot_modules.forms.settings.settings_repository.settings_repository_abstraction import (
    SettingRepositoryAbstraction,
)


settings_repository = SettingsRepository()
settings_repository_abs = SettingRepositoryAbstraction(settings_repository)
