from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.repositories.base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Role)
        
    async def get_by_name(
        self,
        name: str,
    ) -> Role | None:
        result = await self.session.execute(
            select(Role).where(Role.name == name)
        )

        return result.scalar_one_or_none()

    async def name_exists(
        self,
        name: str,
    ) -> bool:
        return await self.get_by_name(name) is not None 