from datetime import UTC, datetime, timedelta

from pydantic import Field

from app.core.config import settings
from app.models.base_document import BaseDocument


def refresh_token_expiry() -> datetime:
    return datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)


class RefreshToken(BaseDocument):
    user_id: str

    token: str

    jti: str

    family_id: str

    expires_at: datetime = Field(default_factory=refresh_token_expiry)

    is_revoked: bool = False

    class Settings:
        name = "refresh_tokens"
