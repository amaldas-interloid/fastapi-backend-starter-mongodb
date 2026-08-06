from app.models.role_permission import RolePermission
from app.repositories.base import BaseRepository


class RolePermissionRepository(
    BaseRepository[RolePermission]
):
    def __init__(self):
        super().__init__(RolePermission)