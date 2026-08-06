from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.config import settings


class MongoDB:
    client: AsyncIOMotorClient | None = None


mongodb = MongoDB()


async def connect_to_mongodb() -> None:
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)

    await init_beanie(
        database=mongodb.client[settings.DATABASE_NAME],
        document_models=[],
    )


async def close_mongodb_connection() -> None:
    if mongodb.client is not None:
        mongodb.client.close()