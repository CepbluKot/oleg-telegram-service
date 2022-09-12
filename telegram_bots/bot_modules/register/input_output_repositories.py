from bot_modules.register.register_repository.register_repository_realisation import (
    RegisterRepository,
    RegisterEditRepository,
    CurrentlyChangingRegisterDataRepository,
)
from bot_modules.register.register_repository.register_repository_abstraction import (
    RegisterRepositoryAbstraction,
    RegisterEditRepositoryAbstraction,
    CurrentlyChangingRegisterDataRepositoryAbstraction,
)


register_repository = RegisterRepository()
register_repository_abs = RegisterRepositoryAbstraction(register_repository)


register_edit_repository = RegisterEditRepository()
register_edit_repository_abs = RegisterEditRepositoryAbstraction(
    register_edit_repository
)


currently_changing_register_data_repository = CurrentlyChangingRegisterDataRepository()
currently_changing_register_data_repository_abs = (
    CurrentlyChangingRegisterDataRepositoryAbstraction(
        currently_changing_register_data_repository
    )
)
