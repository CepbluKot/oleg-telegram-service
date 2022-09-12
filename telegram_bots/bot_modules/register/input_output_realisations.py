from bot_modules.register.register_realisation.register_realisation import (
    RegisterRealisation,
)
from bot_modules.register.register_realisation.register_abstraction import (
    RegisterAbstraction,
)

from bot_modules.register.register_editor_realisation.register_editor_realisation import (
    RegisterEditPrepod,
    RegisterEditStudent,
)
from bot_modules.register.register_editor_realisation.register_editor_abstraction import (
    RegisterEditPrepodAbstraction,
    RegisterEditStudentAbstraction,
)


register = RegisterRealisation()
register_abs = RegisterAbstraction(register)

register_edit_prepod = RegisterEditPrepod()
register_edit_prepod_abs = RegisterEditPrepodAbstraction(register_edit_prepod)

register_edit_student = RegisterEditStudent()
register_edit_student_abs = RegisterEditStudentAbstraction(register_edit_student)
