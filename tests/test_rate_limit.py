from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import settings
from app.db.redis import redis_client
from app.main import app


@pytest.fixture
def mock_redis(monkeypatch):
    incr = AsyncMock(return_value=1)
    expire = AsyncMock(return_value=True)

    monkeypatch.setattr(
        redis_client,
        "incr",
        incr,
    )
    monkeypatch.setattr(
        redis_client,
        "expire",
        expire,
    )

    return incr, expire


@pytest.mark.anyio
async def test_rate_limit_allows_request(mock_redis):
    incr, expire = mock_redis

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200

    incr.assert_awaited_once()
    expire.assert_awaited_once()


@pytest.mark.anyio
async def test_rate_limit_returns_429_when_exceeded(
    monkeypatch,
):
    monkeypatch.setattr(
        redis_client,
        "incr",
        AsyncMock(
            return_value=settings.REDIS_RATE_LIMIT + 1,
        ),
    )

    monkeypatch.setattr(
        redis_client,
        "expire",
        AsyncMock(return_value=True),
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 429

    assert response.json() == {
        "success": False,
        "message": "Rate limit exceeded. Please try again later.",
        "data": None,
    }

    assert response.headers["Retry-After"] == str(
        settings.REDIS_RATE_LIMIT_WINDOW,
    )

@pytest.mark.anyio
async def test_rate_limit_sets_expiration_on_first_request(
    monkeypatch,
):
    incr = AsyncMock(return_value=1)
    expire = AsyncMock(return_value=True)

    monkeypatch.setattr(
        redis_client,
        "incr",
        incr,
    )
    monkeypatch.setattr(
        redis_client,
        "expire",
        expire,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200

    incr.assert_awaited_once()

    expire.assert_awaited_once_with(
        "rate_limit:127.0.0.1",
        60,
    )


@pytest.mark.anyio
async def test_rate_limit_fails_open_when_redis_unavailable(
    monkeypatch,
):
    from redis.exceptions import RedisError

    monkeypatch.setattr(
        redis_client,
        "incr",
        AsyncMock(
            side_effect=RedisError("Redis unavailable"),
        ),
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200



@pytest.mark.anyio
async def test_rate_limit_does_not_reset_expiration(
    monkeypatch,
):
    incr = AsyncMock(
        return_value=settings.REDIS_RATE_LIMIT,
    )

    expire = AsyncMock(return_value=True)

    monkeypatch.setattr(
        redis_client,
        "incr",
        incr,
    )

    monkeypatch.setattr(
        redis_client,
        "expire",
        expire,
    )

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/")

    assert response.status_code == 200

    incr.assert_awaited_once()
    expire.assert_not_awaited()