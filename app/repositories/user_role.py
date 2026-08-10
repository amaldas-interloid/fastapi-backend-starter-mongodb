from app.models.user_role import UserRole
from app.repositories.base import BaseRepository


class UserRoleRepository(BaseRepository[UserRole]):
    def __init__(self) -> None:
        super().__init__(UserRole)

    async def get_by_user_id(
        self,
        user_id: str,
    ) -> list[UserRole]:
        return await self.model.find(
            self.model.user_id == user_id,
        ).to_list()