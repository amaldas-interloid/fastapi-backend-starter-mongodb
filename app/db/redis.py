from redis.asyncio import Redis

from app.core.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


async def connect_to_redis() -> None:
    await redis_client.ping()


async def close_redis_connection() -> None:
    await redis_client.aclose()
