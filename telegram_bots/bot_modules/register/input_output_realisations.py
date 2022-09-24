from bot_modules.register.register_realisation.register_realisation import (
    RegisterForUniversityRealisation,
)
from bot_modules.register.register_realisation.register_abstraction import (
    RegisterForUniversutyAbstraction,
)

from bot_modules.register.register_editor_realisation.register_editor_realisation import (
    RegisterEditPrepod,
    RegisterEditStudent,
)
from bot_modules.register.register_editor_realisation.register_editor_abstraction import (
    RegisterEditPrepodAbstraction,
    RegisterEditStudentAbstraction,
)
from telegram_bots.bot_modules.register.register_realisation.register_abstraction import RegisterForCustomersAbstraction
from telegram_bots.bot_modules.register.register_realisation.register_realisation import RegisterForCustomersInDatabaseRealisation


register_for_university = RegisterForUniversityRealisation()
register_for_university_abs = RegisterForUniversutyAbstraction(register_for_university)

register_for_customers = RegisterForUniversityRealisation()
register_for_customers_abs = RegisterForUniversutyAbstraction(register_for_university)

register_edit_prepod = RegisterEditPrepod()
register_edit_prepod_abs = RegisterEditPrepodAbstraction(register_edit_prepod)

register_edit_student = RegisterEditStudent()
register_edit_student_abs = RegisterEditStudentAbstraction(register_edit_student)


######

register_test = RegisterForCustomersInDatabaseRealisation()
register_test_abs = RegisterForCustomersAbstraction(register_test)
