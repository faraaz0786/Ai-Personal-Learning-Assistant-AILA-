import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.error_utils import safe_error_response
from app.core.exceptions import AppError


logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
        except AppError:
            raise
        except Exception as e:
            logger.error("Unhandled exception in SecurityHeadersMiddleware downstream", exc_info=e)
            response = safe_error_response(
                status_code=500,
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred processing the request.",
            )
            
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response
