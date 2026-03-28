import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from api.core.error_utils import safe_error_response
from api.core.exceptions import AppError
from api.core.security import SecurityContext


logger = logging.getLogger(__name__)


class SessionContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            request.state.session_id = request.cookies.get("aila_session")
            request.state.security_context = SecurityContext(
                session_id=request.state.session_id
            )
            return await call_next(request)
        except AppError:
            raise
        except Exception as e:
            logger.error("Unhandled exception in SessionContextMiddleware downstream", exc_info=e)
            return safe_error_response(
                status_code=500,
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred processing the request.",
            )
