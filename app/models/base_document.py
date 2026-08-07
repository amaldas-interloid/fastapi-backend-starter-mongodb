from uuid import uuid4

from beanie import Document
from pydantic import ConfigDict, Field

from app.models.mixins import SoftDeleteMixin, TimestampMixin


class BaseDocument(
    TimestampMixin,
    SoftDeleteMixin,
    Document,
):
    id: str = Field(default_factory=lambda: str(uuid4()))

    model_config = ConfigDict(
        populate_by_name=True,
    )   

    class Settings:
        use_state_management = True