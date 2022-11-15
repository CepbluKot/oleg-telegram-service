from typing import List
from bot_modules.register.data_structures import User
from register_repository_interface import RegisterRepositoryInterface


class RegisterRepositoryRealisationDatabase(RegisterRepositoryInterface):
    def add_user(self, user: User):
        return self.interface.add_user(user=user)

    
    def check_is_user_registered(self) -> List[User]:
        return self.interface.check_is_user_registered()

    
    def get_user(self, user_id: int) -> User:
        return self.interface.get_user(user_id=user_id)

    
    def update_user(self, user: User):
        return self.interface.update_user(user=user)

    
    def delete_user(self, user_id: int):
        return self.interface.delete_user(user_id=user_id)
