from datetime import UTC, datetime
from typing import Any

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        return await self.model.find_one(
            {
                "email": email,
                "is_deleted": False,
            }
        )

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        return await self.model.find_one(
            {
                "username": username,
                "is_deleted": False,
            }
        )

    async def get_by_id(
        self,
        user_id: str,
    ) -> User | None:
        return await self.model.find_one(
            {
                "_id": user_id,
                "is_deleted": False,
            }
        )

    async def get_all_users(
        self,
        skip: int = 0,
        limit: int = 20,
    ) -> list[User]:
        return await self.model.find(
            {
                "is_deleted": False,
            }
        ).skip(skip).limit(limit).to_list()

    async def count_users(self) -> int:
        return await self.model.find(
            {
                "is_deleted": False,
            }
        ).count()

    async def update_user(
        self,
        user: User,
        data: dict[str, Any],
    ) -> User:
        for key, value in data.items():
            setattr(user, key, value)

        user.updated_at = datetime.now(UTC)

        await user.save()

        return user

    async def soft_delete(
        self,
        user: User,
    ) -> User:
        user.is_deleted = True
        user.deleted_at = datetime.now(UTC)
        user.updated_at = datetime.now(UTC)

        await user.save()

        return user
