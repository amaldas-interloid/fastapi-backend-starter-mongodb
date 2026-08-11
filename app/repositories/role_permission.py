from app.models.role_permission import RolePermission
from app.repositories.base import BaseRepository


class RolePermissionRepository(BaseRepository[RolePermission]):
    def __init__(self) -> None:
        super().__init__(RolePermission)

    async def get_by_role_id(
        self,
        role_id: str,
    ) -> list[RolePermission]:
        return await self.model.find(
            {
                "role_id": role_id,
            }
        ).to_list()

    async def get_by_role_and_permission(
        self,
        role_id: str,
        permission_id: str,
    ) -> RolePermission | None:
        return await self.model.find_one(
            {
                "role_id": role_id,
                "permission_id": permission_id,
            }
        )