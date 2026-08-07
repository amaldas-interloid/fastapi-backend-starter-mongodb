from typing import Annotated

from beanie import Indexed
from pydantic import EmailStr

from app.models.base_document import BaseDocument


class User(BaseDocument):
    email: Annotated[
        EmailStr,
        Indexed(unique=True),
    ]

    username: Annotated[
        str,
        Indexed(unique=True),
    ]

    first_name: str

    last_name: str

    hashed_password: str

    is_active: bool = True

    is_verified: bool = False

    class Settings:
        name = "users"