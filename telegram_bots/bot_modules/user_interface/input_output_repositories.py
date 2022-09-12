from bot_modules.user_interface.ui_repository.ui_repository import (
    CompletingFormsDispatcher,
    SelectedUIRepository,
)
from bot_modules.user_interface.ui_repository.ui_repository_abstraction import (
    CompletingFormsDispatcherAbstraction,
    SelectedUIRepositoryAbstraction,
)


completing_forms_dispatcher = CompletingFormsDispatcher()
completing_forms_dispatcher_abs = CompletingFormsDispatcherAbstraction(
    completing_forms_dispatcher
)

ui_repostiory = SelectedUIRepository()
ui_repostiory_abs = SelectedUIRepositoryAbstraction(ui_repostiory)
