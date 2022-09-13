from typing import List
from bot_modules.service_info.groups_info.groups_repository_interface import (
    GroupsRepositoryInterface,
)


class GroupsRepositoryAbstraction(GroupsRepositoryInterface):
    def __init__(self, interface: GroupsRepositoryInterface) -> None:
        self.interface = interface

    def get_all_groups(self) -> List[str]:
        return self.interface.get_all_groups()

    def get_related_to_prepod_groups(self, user_id: int) -> List[str]:
        return self.interface.get_related_to_prepod_groups(user_id=user_id)

    def get_students_ids_by_groups(self, groups: List[str]):
        return self.interface.get_students_ids_by_groups(groups=groups)
