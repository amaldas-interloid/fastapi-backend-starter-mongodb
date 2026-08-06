from datetime import UTC, datetime

from pydantic import Field


class TimestampMixin:
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )


class SoftDeleteMixin:
    is_deleted: bool = False
    deleted_at: datetime | None = None