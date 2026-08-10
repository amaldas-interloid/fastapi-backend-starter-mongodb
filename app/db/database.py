from beanie import init_beanie
from pymongo import AsyncMongoClient

from app.core.config import settings
from app.models.permission import Permission
from app.models.refresh_token import RefreshToken
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User
from app.models.user_role import UserRole


class MongoDB:
    client: AsyncMongoClient | None = None


mongodb = MongoDB()


async def connect_to_mongodb() -> None:
    mongodb.client = AsyncMongoClient(settings.MONGODB_URL)

    await init_beanie(
        database=mongodb.client[settings.DATABASE_NAME],
        document_models=[
            User,
            Role,
            Permission,
            RefreshToken,
            UserRole,
            RolePermission,
        ],
    )


async def close_mongodb_connection() -> None:
    if mongodb.client is not None:
        await mongodb.client.close()
