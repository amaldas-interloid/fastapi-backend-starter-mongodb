from app.models.base_document import BaseDocument


class RolePermission(BaseDocument):
    role_id: str
    permission_id: str

    class Settings:
        name = "role_permissions"