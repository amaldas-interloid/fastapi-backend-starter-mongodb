from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.db.database import check_mongodb_connection

router = APIRouter()


@router.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "message": "Application is running",
    }


@router.get("/health/ready", tags=["Health"])
async def readiness_check():
    mongodb_ready = await check_mongodb_connection()

    if not mongodb_ready:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "status": "unhealthy",
                "message": "MongoDB is unavailable",
            },
        )

    return {
        "status": "ready",
        "message": "Application is ready",
    }
