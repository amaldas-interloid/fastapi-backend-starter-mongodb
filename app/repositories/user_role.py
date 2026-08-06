from app.models.user_role import UserRole
from app.repositories.base import BaseRepository


class UserRoleRepository(BaseRepository[UserRole]):
    def __init__(self):
        super().__init__(UserRole)