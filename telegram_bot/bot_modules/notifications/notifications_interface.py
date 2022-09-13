from abc import ABC, abstractmethod
from typing import List


class NotificationsInterface(ABC):
    @abstractmethod
    async def new_form_notification(self, list_of_users_ids: List[str]):
        raise NotImplemented

    @abstractmethod
    async def registration_approved(self, user_id: str):
        raise NotImplemented

    @abstractmethod
    async def registration_denied(self, user_id: str):
        raise NotImplemented
