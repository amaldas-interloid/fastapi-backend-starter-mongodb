from datetime import UTC, datetime

from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(BaseRepository[RefreshToken]):
    def __init__(self) -> None:
        super().__init__(RefreshToken)

    async def get_by_token(
        self,
        token: str,
    ) -> RefreshToken | None:
        return await RefreshToken.find_one(RefreshToken.token == token)

    async def get_by_jti(
        self,
        jti: str,
    ) -> RefreshToken | None:
        return await RefreshToken.find_one(
            RefreshToken.jti == jti,
        )

    async def revoke(
        self,
        refresh_token: RefreshToken,
    ) -> RefreshToken:
        refresh_token.is_revoked = True
        await refresh_token.save()
        return refresh_token

    async def is_valid(
        self,
        refresh_token: RefreshToken,
    ) -> bool:
        expires_at = refresh_token.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)

        return not refresh_token.is_revoked and expires_at > datetime.now(UTC)

    async def revoke_family(
        self,
        family_id: str,
    ) -> None:
        await RefreshToken.find(
            RefreshToken.family_id == family_id,
            RefreshToken.is_revoked == False,  # noqa: E712
        ).set(
            {RefreshToken.is_revoked: True},
        )
