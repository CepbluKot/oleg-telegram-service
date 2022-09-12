from bot_modules.forms.forms_realisation.forms_realisation_abstraction import (
    FormsConstructorAbstracton,
    FormsMenuAbstraction,
    FormsEditorAbstraction,
    FormsSenderAbstraction,
)
from bot_modules.forms.forms_realisation.forms_realisation import (
    FormsConstructorRealisation,
    FormsMenuRealisation,
    FormsEditorRealisation,
    FormsSenderRealisation,
)


forms_constructor = FormsConstructorRealisation()
forms_constructor_abs = FormsConstructorAbstracton(forms_constructor)

forms_menu = FormsMenuRealisation()
forms_menu_abs = FormsMenuAbstraction(forms_menu)

forms_editor = FormsEditorRealisation()
forms_editor_abs = FormsEditorAbstraction(forms_editor)

forms_sender = FormsSenderRealisation()
forms_sender_abs = FormsSenderAbstraction(forms_sender)
