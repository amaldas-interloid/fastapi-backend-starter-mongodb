from datetime import UTC, datetime

from beanie.operators import RegEx

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    def _build_user_filters(
        self,
        username: str | None = None,
        email: str | None = None,
        is_active: bool | None = None,
        is_verified: bool | None = None,
    ) -> list:
        filters = [
            self.model.is_deleted == False,  # noqa: E712
        ]

        if username:
            filters.append(
                RegEx(
                    self.model.username,
                    username,
                    options="i",
                ),
            )

        if email:
            filters.append(
                RegEx(
                    self.model.email,
                    email,
                    options="i",
                ),
            )

        if is_active is not None:
            filters.append(
                self.model.is_active == is_active,
            )

        if is_verified is not None:
            filters.append(
                self.model.is_verified == is_verified,
            )

        return filters

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        return await self.model.find_one(
            self.model.email == email,
            self.model.is_deleted == False,  # noqa: E712
        )

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        return await self.model.find_one(
            self.model.username == username,
            self.model.is_deleted == False,  # noqa: E712
        )

    async def get_by_id(
        self,
        user_id: str,
    ) -> User | None:
        return await self.model.find_one(
            self.model.id == user_id,
            self.model.is_deleted == False,  # noqa: E712
        )

    async def get_all_users(
        self,
        skip: int = 0,
        limit: int = 20,
        username: str | None = None,
        email: str | None = None,
        is_active: bool | None = None,
        is_verified: bool | None = None,
        sort_by: str = "created_at",
        sort_order: int = -1,
    ) -> list[User]:
        filters = self._build_user_filters(
            username=username,
            email=email,
            is_active=is_active,
            is_verified=is_verified,
        )

        query = self.model.find(*filters)

        query = query.sort(
            [(sort_by, sort_order)],
        )

        return await query.skip(skip).limit(limit).to_list()

    async def count_users(
        self,
        username: str | None = None,
        email: str | None = None,
        is_active: bool | None = None,
        is_verified: bool | None = None,
    ) -> int:
        filters = self._build_user_filters(
            username=username,
            email=email,
            is_active=is_active,
            is_verified=is_verified,
        )

        return await self.model.find(*filters).count()

    async def update_user(
        self,
        user: User,
        data: dict,
    ) -> User:
        for field, value in data.items():
            setattr(user, field, value)

        await user.save()

        return user

    async def soft_delete(
        self,
        user: User,
    ) -> User:
        user.is_deleted = True
        user.deleted_at = datetime.now(UTC)

        await user.save()

        return user
