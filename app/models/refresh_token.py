from datetime import UTC, datetime, timedelta

from pydantic import Field

from app.models.base_document import BaseDocument


def refresh_token_expiry() -> datetime:
    return datetime.now(UTC) + timedelta(days=7)


class RefreshToken(BaseDocument):
    user_id: str

    token: str

    expires_at: datetime = Field(
        default_factory=refresh_token_expiry
    )

    is_revoked: bool = False

    class Settings:
        name = "refresh_tokens"