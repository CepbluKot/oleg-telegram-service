from pydantic import BaseModel


class Settings(BaseModel):

    message_delete_switch: bool = True
    message_delete_delay: int = 60

    forms_notifications: bool = True

    schedule_notifications_switch: bool = True
    schedule_notifications_delay: int = 15 * 60
