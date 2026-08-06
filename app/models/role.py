from typing import Annotated

from beanie import Indexed

from app.models.base_document import BaseDocument


class Role(BaseDocument):
    name: Annotated[str, Indexed(unique=True)]

    description: str | None = None

    class Settings:
        name = "roles"