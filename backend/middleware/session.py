import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.exceptions import AppError
from core.security import SecurityContext

logger = logging.getLogger(__name__)


class SessionContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            # Attach session + security context
            request.state.session_id = request.cookies.get("aila_session")
            request.state.security_context = SecurityContext(
                session_id=request.state.session_id
            )

            return await call_next(request)

        except AppError:
            # Let FastAPI handle properly
            raise

        except Exception as e:
            # 🔥 CRITICAL: DO NOT HIDE ERROR
            print("🔥 MIDDLEWARE CRASH:", str(e))
            logger.error("Middleware crash", exc_info=True)

            raise e  # ❗ MUST raise, not return response
            