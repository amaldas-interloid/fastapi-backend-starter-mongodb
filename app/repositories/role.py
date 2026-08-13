from app.models.role import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self) -> None:
        super().__init__(Role)

async def get_by_name(
    self,
    name: str,
) -> Role | None:
    return await self.model.find_one(
        {
            "name": name,
        }
    )