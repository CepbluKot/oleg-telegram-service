from typing import List
from bot_modules.notifications.notifications_interface import NotificationsInterface
from bots import student_bot


class Notifications(NotificationsInterface):
    async def new_form_notification(self, list_of_users_ids: List[str]):
        for user_id in list_of_users_ids:
            await student_bot.send_message(
                text="Вы получили новую форму", user_id=user_id
            )

    async def registration_approved(self, user_id: str):
        await student_bot.send_message(
            text="Ваши рег. данные подтверждены", user_id=user_id
        )

    async def registration_denied(self, user_id: str):
        await student_bot.send_message(
            text="Ваши рег. данные отклонены, заново зарегистрируйтесь с верными данными",
            user_id=user_id,
        )
