from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.db.redis import redis_client


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        client_ip = request.client.host if request.client else "unknown"

        redis_key = f"rate_limit:{client_ip}"

        try:
            request_count = await redis_client.incr(redis_key)

            if request_count == 1:
                await redis_client.expire(
                    redis_key,
                    settings.REDIS_RATE_LIMIT_WINDOW,
                )

            if request_count > settings.REDIS_RATE_LIMIT:
                return JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "message": ("Rate limit exceeded. Please try again later."),
                        "data": None,
                    },
                    headers={
                        "Retry-After": str(
                            settings.REDIS_RATE_LIMIT_WINDOW,
                        ),
                    },
                )

        except RedisError:
            # Do not make Redis failure bring down the API.
            # The application can continue without rate limiting.
            return await call_next(request)

        return await call_next(request)
