from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        return await User.find_one({"email": email})

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        return await User.find_one({"username": username})