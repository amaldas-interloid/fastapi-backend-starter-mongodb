from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import logger, setup_logging
from app.db.database import (
    close_mongodb_connection,
    connect_to_mongodb,
)
from app.db.redis import (
    close_redis_connection,
    connect_to_redis,
)
from app.exceptions.exception_handlers import register_exception_handlers
from app.middleware.cors import setup_cors
from app.middleware.process_time import ProcessTimeMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongodb()
    logger.info("MongoDB connected")

    await connect_to_redis()
    logger.info("Redis connected")

    logger.info("Application started")

    yield

    await close_redis_connection()
    logger.info("Redis disconnected")

    await close_mongodb_connection()
    logger.info("MongoDB disconnected")

    logger.info("Application stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)
register_exception_handlers(app)
setup_cors(app)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(ProcessTimeMiddleware)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "message": f"{settings.APP_NAME} is running",
        "version": settings.APP_VERSION,
    }
