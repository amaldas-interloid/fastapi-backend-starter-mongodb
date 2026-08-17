from unittest.mock import patch

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware


def test_request_logging():
    app = FastAPI()

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    @app.get("/test")
    async def test_endpoint():
        return {"status": "ok"}

    client = TestClient(app)

    with patch("app.middleware.request_logging.logger.info") as mock_logger:
        response = client.get("/test")

    assert response.status_code == 200

    mock_logger.assert_called_once()

    log_message = mock_logger.call_args.args[0]

    assert "Request completed" in log_message
