from bot_modules.service_info.groups_info.groups_repository_realisation import (
    GroupsRepositoryRealisation,
)
from bot_modules.service_info.groups_info.groups_repository_abstraction import (
    GroupsRepositoryAbstraction,
)


groups_repository = GroupsRepositoryRealisation()
groups_repository_abs = GroupsRepositoryAbstraction(groups_repository)
