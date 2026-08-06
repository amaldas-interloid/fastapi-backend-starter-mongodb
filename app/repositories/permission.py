from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.permission import Permission
from app.repositories.base import BaseRepository


class PermissionRepository(BaseRepository[Permission]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Permission)

    async def get_by_name(
        self,
        name: str,
    ) -> Permission | None:
        result = await self.session.execute(
            select(Permission).where(Permission.name == name)
        )

        return result.scalar_one_or_none()

    async def name_exists(
        self,
        name: str,
    ) -> bool:
        return await self.get_by_name(name) is not None