import logging
import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        request_id = getattr(request.state, "request_id", "-")

        try:
            response = await call_next(request)

        except Exception:
            process_time = time.perf_counter() - start_time

            logger.exception(
                "Request failed | request_id=%s | method=%s | path=%s "
                "| process_time=%.6fs",
                request_id,
                request.method,
                request.url.path,
                process_time,
            )

            raise

        process_time = time.perf_counter() - start_time

        logger.info(
            "Request completed | request_id=%s | method=%s | path=%s "
            "| status_code=%d | process_time=%.6fs",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time,
        )

        return response