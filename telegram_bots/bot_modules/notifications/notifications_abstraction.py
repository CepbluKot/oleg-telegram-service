from typing import List
from bot_modules.notifications.notifications_interface import NotificationsInterface


class NotificationsAbstraction(NotificationsInterface):
    def __init__(self, interface: NotificationsInterface) -> None:
        self.interface = interface

    async def new_form_notification(self, list_of_users_ids: List[str]):
        return self.interface.new_form_notification(list_of_users_ids=list_of_users_ids)

    async def registration_approved(self, user_id: str):
        return self.interface.registration_approved(user_id=user_id)

    async def registration_denied(self, user_id: str):
        return self.interface.registration_denied(user_id=user_id)
