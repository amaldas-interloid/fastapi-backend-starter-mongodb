from unittest.mock import AsyncMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints.health import router


def create_test_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    return app


def test_health_check():
    app = create_test_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "message": "Application is running",
    }


def test_readiness_check_success():
    app = create_test_app()
    client = TestClient(app)

    with patch(
        "app.api.v1.endpoints.health.check_mongodb_connection",
        new=AsyncMock(return_value=True),
    ):
        response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "message": "Application is ready",
    }


def test_readiness_check_database_unavailable():
    app = create_test_app()
    client = TestClient(app)

    with patch(
        "app.api.v1.endpoints.health.check_mongodb_connection",
        new=AsyncMock(return_value=False),
    ):
        response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unhealthy",
        "message": "MongoDB is unavailable",
    }
