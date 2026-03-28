import logging
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from api.core.error_utils import safe_error_response
from api.core.logging import request_id_ctx_var
from api.core.exceptions import AppError


logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware that generates a unique UUID4 for each incoming request,
    stores it in a ContextVar for downstream logging, and attaches it
    to the response standard headers.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid4())
        
        # Set the context variable so any logger anywhere in the async call stack can find it
        request_id_ctx_var.set(request_id)
        
        # Also attach to request state purely for convenience if explicit access is needed
        request.state.request_id = request_id
        
        try:
            response = await call_next(request)
        except AppError:
            raise
        except Exception as e:
            logger.error("Unhandled exception in RequestIdMiddleware downstream", exc_info=e)
            response = safe_error_response(
                status_code=500,
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred processing the request.",
            )

        # Attach request_id to response headers
        response.headers["X-Request-ID"] = request_id
        return response
