from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.db.database import mongodb


def get_database() -> AsyncIOMotorDatabase:
    if mongodb.client is None:
        raise RuntimeError("MongoDB is not connected.")

    return mongodb.client[settings.DATABASE_NAME]