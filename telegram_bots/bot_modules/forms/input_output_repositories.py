from bot_modules.forms.forms_repository.forms_repository_realisation import (
    FormsConstructorRepositoryRealisation,
    FormsRepositoryRealisation,
    ChoosingGroupsDispatcherRealisation,
    SentFormsRepositoryRealisation,
    CurrentlyEditingFormRepository,
)
from bot_modules.forms.forms_repository.forms_repository_abstraction import (
    FormsConstructorRepositoryAbstraction,
    FormsRepositoryAbstraction,
    ChoosingGroupsDispatcherAbstracction,
    SentFormsRepositoryAbstraction,
    CurrentlyEditingFormRepositoryAbstraction,
)


forms_constructor_repository = FormsConstructorRepositoryRealisation()
forms_constructor_repository_abs = FormsConstructorRepositoryAbstraction(
    forms_constructor_repository
)


forms_repository = FormsRepositoryRealisation()
forms_repository_abs = FormsRepositoryAbstraction(forms_repository)


choosing_groups_dispatcher = ChoosingGroupsDispatcherRealisation()
choosing_groups_dispatcher_abs = ChoosingGroupsDispatcherAbstracction(
    choosing_groups_dispatcher
)


sent_forms_repository = SentFormsRepositoryRealisation()
sent_forms_repository_abs = SentFormsRepositoryAbstraction(sent_forms_repository)


currently_editing_form_repository = CurrentlyEditingFormRepository()
currently_editing_form_repository_abs = CurrentlyEditingFormRepositoryAbstraction(
    currently_editing_form_repository
)
