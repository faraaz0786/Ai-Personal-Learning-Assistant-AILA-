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
            # 🔍 DEBUG: Log incoming request
            print(f"\n🚀 Incoming Request: {request.method} {request.url}")

            # 🔍 DEBUG: Log cookies received
            print("🍪 Incoming Cookies:", request.cookies)

            # Extract session
            session_id = request.cookies.get("aila_session")

            # 🔍 DEBUG: Log session ID
            print("🆔 Extracted Session ID:", session_id)

            # Attach to request state
            request.state.session_id = session_id
            request.state.security_context = SecurityContext(
                session_id=session_id
            )

            response = await call_next(request)

            # 🔍 DEBUG: Log response status
            print(f"✅ Response Status: {response.status_code}\n")

            return response

        except AppError as e:
            # ✅ Proper app-level error logging
            print("⚠️ AppError Triggered:", e.code, e.message)
            logger.warning("AppError in middleware", exc_info=True)
            raise

        except Exception as e:
            # 🔥 CRITICAL: FULL TRACE VISIBILITY
            print("🔥 MIDDLEWARE CRASH:", str(e))
            logger.error("Middleware crash", exc_info=True)
            raise  # ❗ DO NOT SWALLOW