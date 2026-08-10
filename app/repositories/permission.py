from app.models.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self) -> None:
        super().__init__(Permission)

    async def get_by_name(self, name: str) -> Permission | None:
        return await self.model.find_one(
            self.model.name == name,
        )