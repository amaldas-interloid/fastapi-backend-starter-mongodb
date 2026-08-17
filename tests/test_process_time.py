from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.process_time import ProcessTimeMiddleware


def test_process_time_header():
    app = FastAPI()
    app.add_middleware(ProcessTimeMiddleware)

    @app.get("/test")
    async def test_endpoint():
        return {"status": "ok"}

    client = TestClient(app)

    response = client.get("/test")

    assert response.status_code == 200
    assert "X-Process-Time" in response.headers

    process_time = float(response.headers["X-Process-Time"])

    assert process_time >= 0
