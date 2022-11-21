from telegram_bots.modules.register.repository.output import (
    register_repository_abstraction,
)


class RegisterBackend:
    async def update_users_registration(self, phone_number: str, telegram_id: int):
        try:
            user_data = await register_repository_abstraction.get_user(telegram_id)
            user_data.phone = phone_number
            print("ok ok im working")
            # await register_repository_abstraction.update_user(user_data)

        except:
            print("error - update_users_registration")
