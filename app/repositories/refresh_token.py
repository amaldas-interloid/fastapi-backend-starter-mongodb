from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, RefreshToken)

    async def get_by_token(
        self,
        token: str,
    ) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshToken).where(
                RefreshToken.token == token
            )
        )

        return result.scalar_one_or_none()

    async def revoke(
        self,
        token: RefreshToken,
    )->None:
        token.is_revoked = True
        await self.session.flush()

    async def revoke_all_for_user(
        self,
        user_id: UUID,
    ) -> None:
        await self.session.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id)
            .values(is_revoked=True)
        )

        await self.session.flush()

    async def delete_expired(self) -> None:
        await self.session.execute(
            delete(RefreshToken).where(
                RefreshToken.expires_at < datetime.now(UTC)
            )
        )

        await self.session.flush()