from app.models.base_document import BaseDocument


class UserRole(BaseDocument):
    user_id: str
    role_id: str

    class Settings:
        name = "user_roles"