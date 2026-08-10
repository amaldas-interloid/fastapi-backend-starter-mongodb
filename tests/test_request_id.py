import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from app.middleware.request_id import RequestIDMiddleware


@pytest.mark.anyio
async def test_request_id_is_added():
    app = FastAPI()
    app.add_middleware(RequestIDMiddleware)

    @app.get("/test")
    async def test_endpoint(request: Request):
        assert request.state.request_id
        return {"status": "ok"}

    client = TestClient(app)

    response = client.get("/test")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]