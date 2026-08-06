from app.models.refresh_token import RefreshToken
from app.repositories.base import BaseRepository


class RefreshTokenRepository(
    BaseRepository[RefreshToken]
):
    def __init__(self):
        super().__init__(RefreshToken)

    async def get_by_token(
        self,
        token: str,
    ) -> RefreshToken | None:
        return await RefreshToken.find_one(
            RefreshToken.token == token
        )