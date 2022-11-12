from aiogram import Dispatcher, types
from bot_modules.user_interface.ui_handlers.ui_handlers import PrepodHandlersStatus, StudentHandlersStatus
from bot_modules.user_interface.ui_handlers.ui_handlers_abstraction import PrepodHandlersStatusAbstraction, StudentHandlersStatusAbstraction


def create_form_creator_ui_handlers(dp: Dispatcher):
    form_creator_ui_handlers = PrepodHandlersStatus()
    form_creator_ui_handlers_abs = PrepodHandlersStatusAbstraction(form_creator_ui_handlers)
    return form_creator_ui_handlers_abs.register_handlers_prepod_status(dp)

def create_client_ui_handlers(dp: Dispatcher):
    client_ui_handlers = StudentHandlersStatus()
    client_ui_handlers_abs = StudentHandlersStatusAbstraction(client_ui_handlers)
    return client_ui_handlers_abs.register_handlers_student_status(dp)
