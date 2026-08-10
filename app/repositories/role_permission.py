from app.models.role_permission import RolePermission
from app.repositories.base import BaseRepository


class RolePermissionRepository(
    BaseRepository[RolePermission]
):
    def __init__(self) -> None:
        super().__init__(RolePermission)

    async def get_by_role_id(
        self,
        role_id: str,
    ) -> list[RolePermission]:
        return await self.model.find(
            self.model.role_id == role_id,
        ).to_list()