"""Sliding-window rate limiter middleware backed by Redis."""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from api.core.error_utils import safe_error_response
from api.core.redis import get_client
from api.core.exceptions import AppError

logger = logging.getLogger(__name__)


# Rate limit rules: (path_prefix, key_suffix, max_requests, window_seconds)
_ROUTE_LIMITS: list[tuple[str, str, int, int]] = [
    ("/api/v1/learn/explain", "explain", 10, 60),
    ("/api/v1/learn/quiz", "quiz", 5, 60),
]
_GLOBAL_LIMIT = 60  # requests per minute per IP
_GLOBAL_WINDOW = 60  # seconds


def _get_client_ip(request: Request) -> str:
    """Extract the real client IP, respecting X-Forwarded-For behind a proxy."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip non-API and safe methods
        if request.method in ("GET", "HEAD", "OPTIONS") or not request.url.path.startswith("/api/"):
            try:
                return await call_next(request)
            except AppError:
                raise
            except Exception as e:
                logger.error("Unhandled exception in RateLimiterMiddleware downstream", exc_info=e)
                return safe_error_response(
                    status_code=500,
                    code="INTERNAL_SERVER_ERROR",
                    message="An unexpected error occurred processing the request.",
                )

        client = get_client()
        if client is None:
            # Redis unavailable → fail open (no rate limiting)
            try:
                return await call_next(request)
            except AppError:
                raise
            except Exception as e:
                logger.error("Unhandled exception in RateLimiterMiddleware downstream", exc_info=e)
                return safe_error_response(
                    status_code=500,
                    code="INTERNAL_SERVER_ERROR",
                    message="An unexpected error occurred processing the request.",
                )

        client_ip = _get_client_ip(request)
        session_id = request.cookies.get("aila_session", client_ip)

        try:
            # --- Per-route limits ---
            for path_prefix, suffix, max_req, window in _ROUTE_LIMITS:
                if request.url.path.startswith(path_prefix):
                    route_key = f"rate:{session_id}:{suffix}"
                    blocked = await self._check_limit(route_key, max_req, window)
                    if blocked is not None:
                        return blocked
                    break  # matched a route, skip remaining

            # --- Global IP limit ---
            ip_key = f"rate:ip:{client_ip}"
            blocked = await self._check_limit(ip_key, _GLOBAL_LIMIT, _GLOBAL_WINDOW)
            if blocked is not None:
                return blocked

        except Exception as exc:
            # Redis error → fail open
            logger.warning("Rate limiter error: %s", exc)

        try:
            return await call_next(request)
        except AppError:
            raise
        except Exception as e:
            logger.error("Unhandled exception in RateLimiterMiddleware downstream", exc_info=e)
            return safe_error_response(
                status_code=500,
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred processing the request.",
            )

    @staticmethod
    async def _check_limit(key: str, max_requests: int, window: int) -> JSONResponse | None:
        """Increment the counter and check if the limit is exceeded.

        Returns a 429 JSONResponse if exceeded, or None if within limits.
        Uses INCR + EXPIRE for a simple sliding window.
        """
        client = get_client()
        if client is None:
            return None

        current = await client.incr(key)
        if current == 1:
            await client.expire(key, window)

        if current > max_requests:
            ttl = await client.ttl(key)
            retry_after = max(ttl, 1)
            logger.info("Rate limited: %s (%d/%d)", key, current, max_requests)
            return JSONResponse(
                status_code=429,
                content={
                    "error": {
                        "code": "RATE_LIMITED",
                        "message": "Rate limit exceeded. Please try again later.",
                        "detail": {"retry_after": retry_after},
                    }
                },
                headers={"Retry-After": str(retry_after)},
            )

        return None
