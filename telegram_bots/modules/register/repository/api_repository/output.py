from telegram_bots.modules.register.repository.api_repository.repository_realisation import (
    RegisterRepositoryRealisationDatabase,
)
from telegram_bots.modules.register.repository.api_repository.repository_abstraction import (
    RegisterRepositoryAbstraction,
)


__realisation = RegisterRepositoryRealisationDatabase()
register_repository_abstraction = RegisterRepositoryAbstraction(__realisation)
