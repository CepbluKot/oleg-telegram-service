from abc import abstractmethod, ABC
from typing import List


class GroupsRepositoryInterface(ABC):
    @abstractmethod
    def get_all_groups() -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_related_to_prepod_groups(self, user_id: int) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_students_ids_by_groups(self, groups: List[str]) -> List[str]:
        raise NotImplementedError
